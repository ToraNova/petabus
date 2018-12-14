package altf4.bustalk;

import android.os.AsyncTask;
import android.util.Log;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class NetworkManager extends AsyncTask<Void, Void, String> {
    //declare and initialise
    private String buffer = "";
    private String urlString;
    private String type;
    private URL url;
    private HttpURLConnection connection = null;
    private static final String DebugTag = "DEV_HTTP_DEBUG_MSG";
    //private Context context;
    public login loginActivity;
    public push pushActivity;

    //constructor
    public NetworkManager(String u, String t) {
        this.urlString = u;
        this.type = t;
    }

    public NetworkManager(){
        this.urlString = "";
        this.type = "";
    }

    /*
    public NetworkManager(Context context){
         this.context = context;
    }
    */

    protected String doInBackground(Void... params) {
        Log.d(DebugTag, urlString + "\t" + type);
        try {
            //connect to the url
            url = new URL(urlString);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setDoInput(true);
            connection.connect();

            InputStream in = connection.getInputStream();
            InputStreamReader isw = new InputStreamReader(in);

            //read status of pushing data to the web server
            int data = isw.read();

            while (data != -1) {
                char current = (char) data;
                data = isw.read();
                buffer += current;      //includes feedback
            }
            Log.d(DebugTag, "in netman, buffer: " + buffer);
        } catch (Exception e) {
            // Writing exception to log
            e.printStackTrace();
            Log.d(DebugTag, "URL: " + urlString);
            Log.d(DebugTag, "Error in pushing location data:   " + e.toString());
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
        return buffer;
    }

    protected void onPostExecute(String result) {
        Log.d(DebugTag, "Push status: " + result);

        try {
            if (urlString.contains("verify")) {
                Log.d(DebugTag, "verifying");

                if (result.equals("0")) {
                    //pass values to next activity and go to next activity if push was successful
                    loginActivity.sendValuesToNextActivity();
                    loginActivity.login2push();
                } else {
                    //otherwise display error message on screen
                    loginActivity.changeStatusText();
                }
            } else {
                if (urlString.contains("get_rating")) {
                    Log.d(DebugTag, "outputting feedback");
                    pushActivity.outputRating(result);
                }
            }
        }
        catch(Exception e){
            e.printStackTrace();
            Log.d(DebugTag, "Error due to no result: " + e.toString());
        }
    }

    public void setType(String t){
        this.type = t;
    }

    public void setUrl(String u){
        this.urlString = u;
    }

    /*
    private void sendValuesToNextActivity() {
        Intent passIntent = new Intent(loginActivity, push.class);
        passIntent.putExtra("driver_id", loginActivity.getDriver_id());
        passIntent.putExtra("bus_number", loginActivity.getBus_number());
        passIntent.putExtra("ip_address", loginActivity.getIp_address());
        context.startActivity(passIntent);
    }

    //goes to next activity
    public void login2push() {
        Intent intent = new Intent(loginActivity, push.class);
        context.startActivity(intent);
    }
    */
}









