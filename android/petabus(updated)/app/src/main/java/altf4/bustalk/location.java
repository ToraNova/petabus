package altf4.bustalk;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.util.Log;

import java.util.List;

import static android.content.Context.LOCATION_SERVICE;

public class location {
    public final static String DebugTag = "DEBUG_location";
    private static final long MIN_DISTANCE_CHANGE_FOR_UPDATES = 10; // 10 meters
    private static final long MIN_TIME_BW_UPDATES = 1000 * 60 * 1; // 1 minute

    boolean isNetwork_Location = false;
    boolean isGPS_Location = false;
    private Location currentLocation;
    private double longitude;
    private double latitude;
    private Context context;
    public Activity activity;

    // empty constructor
    public location(Context c, Activity a) {
        context = c;
        activity = a;
    }

    // permission checking
    public void checkPermission(LocationManager locman) {
        // if not granted location and internet permissions
        if (!checkLocationPermission()) {
            requestLocationAndInternetPermissions();
        }
        // if location and internet permissions are granted
        else {
        Log.d(DebugTag, "Permission for Fine Location and Internet are granted");

        // enable the respective providers
        isGPS_Location = locman.isProviderEnabled(LocationManager.GPS_PROVIDER);
        isNetwork_Location = locman.isProviderEnabled(LocationManager.NETWORK_PROVIDER);

        locman.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                MIN_TIME_BW_UPDATES,
                MIN_DISTANCE_CHANGE_FOR_UPDATES, new AltF4_LocationListener());

        // debug
        String gpsind = isGPS_Location ? "GPS" : "NO GPS";
        String netind = isNetwork_Location ? "Network" : "NO Network";
        Log.d(DebugTag, gpsind);
        Log.d(DebugTag, netind);

        currentLocation = locman.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            if (currentLocation == null) {
                Log.d(DebugTag, "Null location on start");
            } else {
                longitude = currentLocation.getLongitude();
                latitude = currentLocation.getLatitude();
            }
        }
    }

    // check whether location and internet permissions are granted
    public boolean checkLocationPermission() {
        String permission1 = "android.permission.ACCESS_FINE_LOCATION";
        String permission2 = "android.permission.INTERNET";

        int res1 = context.checkCallingOrSelfPermission(permission1);
        int res2 = context.checkCallingOrSelfPermission(permission2);
        Log.d(DebugTag, "permissions: " + res1 + "\t" + res2);
        return (res1 == PackageManager.PERMISSION_GRANTED && res2 == PackageManager.PERMISSION_GRANTED);
    }

    private void requestLocationAndInternetPermissions(){
        Log.d(DebugTag, "check: " + ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) + "\t" + PackageManager.PERMISSION_GRANTED);

        // if fine location permission specified in manifest, request for user to grant permission
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Log.d(DebugTag, "No permission on Fine location");
            ActivityCompat.requestPermissions(activity, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
        }

        // if internet permission specified in manifest, request for user to grant permission
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED) {
            Log.d(DebugTag, "No permission on Internet");
            ActivityCompat.requestPermissions(activity, new String[]{Manifest.permission.INTERNET}, 1);
        }
        checkLocationPermission();
    }

    public class AltF4_LocationListener implements LocationListener {
        @Override
        public void onLocationChanged(Location location) {
            Log.d(DebugTag, "Location change : Latitude :" + location.getLatitude() + " Longitude :" + location.getLongitude());
        }

        @Override
        public void onProviderDisabled(String provider) {
        }

        @Override
        public void onProviderEnabled(String provider) {
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
        }
    }

    private Location getLastKnownLocation(LocationManager locman) {
        // if not granted location and internet permissions
        if (!checkLocationPermission()) {
            requestLocationAndInternetPermissions();
        } else {
            Log.d(DebugTag, "Android persistent permission check");
        }

        // access location service
        locman = (LocationManager) context.getApplicationContext().getSystemService(LOCATION_SERVICE);
        List<String> providers = locman.getProviders(true);
        Location bestLocation = null;

        // find best location data from the many location data obtained using different providers
        for (String provider : providers) {
            Location l = locman.getLastKnownLocation(provider);
            if (l == null) {
                continue;
            }
            if (bestLocation == null || l.getAccuracy() < bestLocation.getAccuracy()) {
                bestLocation = l;
            }
        }
        Log.d(DebugTag, "current location: " + bestLocation);
        return bestLocation;
    }

    //send latest location to web server
    public void SendLocation(LocationManager locman, networkManager netman, String ip_address,
                             String driver_id, String bus_number, String route) {

        currentLocation = getLastKnownLocation(locman);
        Log.d(DebugTag, "debugging tag 0000002");
        if (currentLocation == null) {
            Log.d(DebugTag, "currentLocation is NULL on starting send");
        } else {
            //separate longitude and latitude of location and display them on screen
            longitude = currentLocation.getLongitude();
            latitude = currentLocation.getLatitude();
            Log.d(DebugTag, "Lat: " + latitude + "\nLong: " + longitude);
            Log.d(DebugTag, "debugging tag 0000003");
            //prepare the URL to push data to web server
            /*String startURL = "http://" + ip_address + "/bustalk/server.php";*/
            String startURL = "http://" + ip_address + ":8000/push/bus/location/begin";
            String parameters = "f0=" + bus_number + "&f1=" + driver_id + "&f2=" + route +
                    "&f3=" + Double.toString(longitude) + "&f4=" + Double.toString(latitude);
            String testURL = startURL + "?" + parameters;
            Log.d(DebugTag, testURL);


            //push required information to the web server
            //netmanExecution(netman, "POST", testURL, parameters, startURL, true, netman);
            netman.setUrlString(testURL);
            netman.setUrlMini(startURL);
            netman.setParam(parameters);
            netman.setType("GET");
            Log.d(DebugTag, "debugging tag 0000004");
            netman.execute();

        }
    }

    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case 1: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                } else {
                    // permission denied, boo! Disable the functionality that depends on this permission.
                }
                return;
            }
            // other 'case' lines to check for other permissions this app might request
        }
    }

    /*
    private void netmanExecution(networkManager netman, String t, String u, String para, String mini,boolean lala, Activity activity){
        netman = new networkManager(u, t, para, mini, lala, activity);
        netman.execute();
    }*/
}
