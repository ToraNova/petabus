package altf4.bustalk;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.view.animation.LinearInterpolator;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.ArrayList;

public class sendLoc_activity extends AppCompatActivity {
    //declaration of variables and constants
    public static final String DebugTag = "DEBUG_sendLoc";
    public static final int period = 1000;     //for sending location periodically
    public static String PACKAGE_NAME;

    private String driver_id = "AD82733";
    private String ip_address = "10.100.19.114";
    private String response = "bus_id=WWW1234,TWI432,JSA8989;route=1,2,3,4;";
    private Spinner spinnerRouteNum;
    private Spinner spinnerBusId;
    private ArrayAdapter<String> adapterBusId;
    private ArrayAdapter<String> adapterRoute;
    private ArrayList<String> bus_id_list = new ArrayList<String>();
    private ArrayList<String> route_list = new ArrayList<String>();
    private ImageView imgSendingLoc;
    private Button sendLoc_button;
    private String selectedBusId;
    private String selectedRouteNum;
    private int count;
    private Runnable sendRunnableCode;
    private Handler sendHandler;
    private Animation animation;
    private AlphaAnimation alphaAnim;
    private networkManager netman;
    private LocationManager locman;
    private Activity activity;
    private location locationFunc;
    private boolean send = false;

    public static final String SHARED_PREF = "sharedPrefs";
    public static final String SAVED_BUS_ID = "520";
    public static final String SAVED_ROUTE = "Route_1";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //set view upon entering this interface
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_push);

        //receive values from previous activity
        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        driver_id = bundle.getString("driver_id");
        ip_address = bundle.getString("ip_address");
        response = bundle.getString("response");
        Log.d(DebugTag, "Driver id: " + driver_id + "\t IP: " + ip_address + "\t response: " + response);

        // process response from server to know valid bus ids and route nums
        processResponse();

        //        netman = new networkManager(this);

        count = 0;
        PACKAGE_NAME = getApplicationContext().getPackageName();
        activity = this;
        locationFunc = new location(this, activity);
        locman = (LocationManager) this.getSystemService(LOCATION_SERVICE);
        locationFunc.checkPermission(locman);

        alphaAnim = new AlphaAnimation(0, (float) 0.5);

        // map xml to java
        spinnerBusId = findViewById(R.id.spinnerBusId);
        spinnerRouteNum = findViewById(R.id.spinnerRouteNum);
        imgSendingLoc = findViewById(R.id.imgSending);
        sendLoc_button = findViewById(R.id.btnSend);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // set up spinners
        //adapterBusId = ArrayAdapter.createFromResource(this, R.array.busId, android.R.layout.simple_spinner_item);
        adapterBusId = new ArrayAdapter<String>(getApplicationContext(), R.layout.spinner_item, bus_id_list);
        adapterBusId.setDropDownViewResource(R.layout.spinner_dialog);
        spinnerBusId.setAdapter(adapterBusId);

        adapterRoute = new ArrayAdapter<String>(getApplicationContext(), R.layout.spinner_item, route_list);
        adapterRoute.setDropDownViewResource(R.layout.spinner_dialog);
        spinnerRouteNum.setAdapter(adapterRoute);

        // set default values
        spinnerBusId.setSelection(0);
        spinnerRouteNum.setSelection(0);

        // update selected bus id and selected route whenever needed
        spinnerBusId.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView <?> parent, View view, int position, long id) {
                selectedBusId = (parent.getItemAtPosition(position)).toString();
            }

            @Override
            public void onNothingSelected(AdapterView <?> parent) {
                selectedBusId = (parent.getItemAtPosition(0)).toString();
            }
        });
        spinnerRouteNum.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView <?> parent, View view, int position, long id) {
                selectedRouteNum = (parent.getItemAtPosition(position)).toString();
            }

            @Override
            public void onNothingSelected(AdapterView <?> parent) {
                selectedRouteNum = (parent.getItemAtPosition(0)).toString();
            }
        });



        // when login_activity button is clicked
        sendLoc_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String buttonText = (sendLoc_button.getText()).toString();
                Log.d(DebugTag, "send button pressed: " + buttonText);

                // display "stop" on button while location is being sent
                if (buttonText.equals("BEGIN")) {
                    send = true;
                    if (locationFunc.checkLocationPermission()) {
                        sendLoc_button.setText(getResources().getIdentifier("@string/stop", "string", PACKAGE_NAME));
                        Log.d(DebugTag, "bus id: " + selectedBusId + "\t route num: " + selectedRouteNum);

                        // disable spinners (cannot change value on spinners) while location is being sent
                        spinnerBusId.setEnabled(false);
                        spinnerRouteNum.setEnabled(false);

                        // send location repeatedly with fixed duration until stop button is clicked
                        setupHandler();
                    }
                    // Start the initial runnable task by posting through the handler
                    Log.d(DebugTag, "periodically run send location task");
                    sendHandler.post(sendRunnableCode);
                } else {
                    // display "send" on button while location is not being sent
                    if (buttonText.equals("STOP")) {
                        stopSendingLoc();
                    }
                }
                Log.d(DebugTag, "sendLoc_activity activity created");
            }
        });
    }

    @Override
    protected void onDestroy(){
        Log.d(DebugTag, "app destroyed");

        // if location is being sent when app is destroyed, stop sending location and log out
        String buttonText = (sendLoc_button.getText()).toString();
        if(buttonText.equals("STOP")) {
            stopSendingLoc();
        }
        Log.d(DebugTag, "stop sending location");
        logOut();

        super.onDestroy();
    }

    private void processResponse(){
        // extract bus ids
        String temp = "";
        int start = response.indexOf("=");
        int end = response.indexOf(";");
        Log.d(DebugTag, "start: " + start + "\t end: " + end);
        int from = start + 1;

        for(int i = start + 1; i <= end; i++){
            if (response.charAt(i) == ',' || response.charAt(i) == ';'){
                temp = response.substring(from, i);
                from = i + 1;
                Log.d(DebugTag, "Bus ID: " + temp + "\t i = " + i);

                bus_id_list.add(temp);
                Log.d(DebugTag, temp + " added into list");
            }
        }

        // extract route numbers
        start = response.lastIndexOf("=");
        end = response.lastIndexOf(";");
        Log.d(DebugTag, "start: " + start + "\t end: " + end);
        from = start + 1;

        for(int i = start + 1; i <= end; i++){
            if (response.charAt(i) == ',' || response.charAt(i) == ';'){
                temp = response.substring(from, i);
                from = i + 1;
                Log.d(DebugTag, "Route num: " + temp);

                route_list.add(temp);
                Log.d(DebugTag, temp + " added into adapter");
            }
        }
    }

    private void stopSendingLoc(){
        send = false;
        sendLoc_button.setText(getResources().getIdentifier("@string/send", "string", PACKAGE_NAME));

        imgSendingLoc.setVisibility(View.INVISIBLE);

        // enable spinners (can change value on spinners) when location is not being sent
        spinnerBusId.setEnabled(true);
        spinnerRouteNum.setEnabled(true);

        // stop sending location
        sendHandler.removeCallbacks(sendRunnableCode);

        // prepare the URL to push data to web server
        String startURL = "http://" + ip_address + ":8000/push/bus/location/logout";
        String testURL = startURL + "?f0=" + driver_id;
        Log.d(DebugTag, "Logout: " + testURL);

        // push required information to the web server
        netman = new networkManager(activity);
        netman.setType("GET");
        netman.setUrlString(testURL);
        netman.setUrlMini(startURL);
        netman.setDriverId(driver_id);
        netman.setIp(ip_address);
        netman.execute();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.sendloc_option, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // action bar will automatically handle clicks on top toolbar
        int id = item.getItemId();

        if (id == R.id.action_save) {
            Log.d(DebugTag, "save settings pressed");
            saveData();
            return true;
        }
        else{
            if (id == R.id.action_load) {
                Log.d(DebugTag, "load settings pressed");
                if(send){
                    Toast.makeText(this, "Data cannot be loaded when location is being sent", Toast.LENGTH_SHORT).show();
                }
                else {
                    loadData();
                }
                return true;
            }
            else {
                if (id == R.id.action_logout) {
                    Log.d(DebugTag, "log out pressed");

                    String buttonText = (sendLoc_button.getText()).toString();
                    if(buttonText.equals("STOP")) {
                        stopSendingLoc();
                    }
                    Log.d(DebugTag, "stop sending location");
    /*
                    // prepare the URL to push data to web server
                    String startURL = "http://" + ip_address + ":8000/push/bus/location/logout";
                    //String testURL = startURL + "?f0=" + driver_id + "&bus_id=" + selectedBusId + "&route=" + selectedRouteNum;
                    String testURL = startURL + "?f0=" + driver_id;
                    Log.d(DebugTag, "Logout: " + testURL);

                    // push required information to the web server
                    netman = new networkManager(activity);
                    netman.setType("GET");
                    netman.setUrlString(testURL);
                    netman.setUrlMini(startURL);
                    netman.setDriverId(driver_id);
                    netman.setIp(ip_address);
                    netman.execute();
*/
                    logOut();
                }
            }
        }
        return super.onOptionsItemSelected(item);
    }

    private void saveData(){
        // no other app can change the shared prefs
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        editor.putString(SAVED_BUS_ID, selectedBusId);
        editor.putString(SAVED_ROUTE, selectedRouteNum);
        editor.apply();

        Toast.makeText(this, "Data Saved", Toast.LENGTH_SHORT).show();
    }

    public void loadData(){
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF, MODE_PRIVATE);

        if ((adapterBusId.getPosition(selectedBusId) != -1) && (adapterRoute.getPosition(selectedRouteNum) != -1)) {
            selectedBusId = sharedPreferences.getString(SAVED_BUS_ID, "");
            selectedRouteNum = sharedPreferences.getString(SAVED_ROUTE, "");

            Toast.makeText(this, "Data Loaded", Toast.LENGTH_SHORT).show();

            updateViews();
        }
        else{
            Toast.makeText(this, "The data is not valid at the moment", Toast.LENGTH_SHORT).show();
        }
    }

    public void updateViews(){
        spinnerBusId.setSelection(adapterBusId.getPosition(selectedBusId));
        spinnerRouteNum.setSelection(adapterRoute.getPosition(selectedRouteNum));

        Log.d(DebugTag, "views updated");
    }

    private void logOut(){
        Log.d(DebugTag, "log out pressed");
        // go back to login activity
        Intent intent = new Intent(this, login_activity.class);
        startActivity(intent);
        // prevent back press to lead back to this activity once logged out
        finish();
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

    private void setupHandler(){
        sendHandler = new Handler();
        sendRunnableCode = new Runnable() {
            @Override
            public void run() {
                Log.d(DebugTag, "Repeating, count = " + count++);

                // show image to indiciate location is being sent
                imgSendingLoc.setVisibility(View.VISIBLE);
                // make image blink
                animation = alphaAnim;                                      // Change alpha from invisible to visible
                animation.setDuration(period);                              // duration
                animation.setInterpolator(new LinearInterpolator());        // do not alter animation rate
                animation.setRepeatCount(Animation.ABSOLUTE);               // Repeat animation
                animation.setRepeatMode(Animation.REVERSE);
                imgSendingLoc.startAnimation(animation);
                Log.d(DebugTag, "debugging tag 0000001");

                netman = new networkManager(activity);
                locationFunc.SendLocation(locman, netman, ip_address, driver_id, selectedBusId, selectedRouteNum);
                // Repeat this the same runnable code block every 3s
                Log.d(DebugTag, "wait for period");
                sendHandler.postDelayed(sendRunnableCode, period);
            }
        };
    }
}
