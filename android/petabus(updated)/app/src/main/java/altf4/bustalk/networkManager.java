package altf4.bustalk;

import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class networkManager extends AsyncTask<Void, Void, String> {
    //declare and initialise
    private String buffer = "";
    private String urlString;
    private String type;
    private String driver_id;
    private String ip_address;
    private String param;
    private String urlmini;
    private URL url;
    private String inputLine = "";
    private HttpURLConnection connection = null;
    private static final String DebugTag = "DEV_HTTP_DEBUG_MSG";
    private login loginActivity;

    //constructor
    public networkManager(){
        this.urlString = "";
        this.type = "";
    //    this.param = "";
    //    this.urlmini = "";
    }
    public networkManager(String u, String t, String id, String ip) {
        this.urlString = u;
        this.type = t;
        this.driver_id = id;
        this.ip_address = ip;
    //    this.param = p;
    //    this.urlmini = a;
    }
    public networkManager(String u, String t, String param, String mini, boolean haha) {
        this.urlString = u;
        this.type = t;
        this.param = param;
        this.urlmini =  mini;
    }

    public networkManager(String a, String b, String c, String d, String e, String f) {
        this.urlString = a;
        this.type = b;
        this.driver_id = c;
        this.ip_address = d;
        this.param = e;
        this.urlmini = f;
    }

    protected String doInBackground(Void... params) {
        Log.d(DebugTag, urlString + "\t  (^o^)(^o^)(^o^)" + type);
        Log.d(DebugTag,  param+ "\t  (^o^)" + type);
        Log.d(DebugTag,  urlmini+ "\t  (^o^)" + type);

        // GET method
        if(type == "GET") {
            try {
                // connect to the url
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
        }
        // POST method
        else{
            try {
                String urlParameters  = param;
                byte[] postData       = urlParameters.getBytes( StandardCharsets.UTF_8 );
                int    postDataLength = postData.length;
                String request        = urlmini;
                URL    url            = new URL( request );
                HttpURLConnection conn= (HttpURLConnection) url.openConnection();
                conn.setDoOutput( true );
                conn.setInstanceFollowRedirects( false );
                conn.setRequestMethod( "POST" );
                conn.setRequestProperty( "Content-Type", "application/x-www-form-urlencoded");
                conn.setRequestProperty( "charset", "utf-8");
                conn.setRequestProperty( "Content-Length", Integer.toString(postDataLength));
                conn.setUseCaches( false );

                conn.setDoOutput(true);
                conn.setDoInput(true);

                // Send POST request
                try(DataOutputStream wr = new DataOutputStream( conn.getOutputStream())){
                    wr.write(postData);
                }
                //wr.writeBytes(param);
                //wr.flush();
                //wr.close();


                System.out.println("\nSending 'POST' request to URL : " + url);
                System.out.println("Post parameters : " + param);

                BufferedReader in =
                        new BufferedReader(new InputStreamReader(conn.getInputStream()));
                // String inputLine;
                StringBuffer response = new StringBuffer();

                //       InputStream in2 = connection.getInputStream();
                //       InputStreamReader isw = new InputStreamReader(in2);

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                //       System.out.println(response.toString() + "HAHAHAHAHAHA");

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
        }
        //return buffer;
        return inputLine;
    }

    // run automatically after doInBackground
    protected void onPostExecute(String result) {
        Log.d(DebugTag, "Push status: " + result);

        try {
            if (urlString.contains("verify")) {
                Log.d(DebugTag, "verifying");
                //loginActivity.nextActivity(result);

                // pass values to next activity and go to next activity if push was successful
                if (result.equals("0")) {
                    // pass values in this activity to the next activity
                    Intent passIntent = new Intent(loginActivity, sendLoc.class);
                    passIntent.putExtra("driver_id", driver_id);
                    passIntent.putExtra("ip_address", ip_address);
                    // for post method response from server
                    passIntent.putExtra("response", inputLine);
                    Log.d(DebugTag, "sending values to next activity");
                    loginActivity.startActivity(passIntent);

                    // goes to next activity
                    Intent intent = new Intent(loginActivity, sendLoc.class);
                    Log.d(DebugTag, "moving to next activity");
                    loginActivity.startActivity(intent);
                    loginActivity.finish();      // disable "back" to go back to login page

                    Log.d(DebugTag, "pushing to web server");
                }
                // otherwise display error message on screen
                else {
                    loginActivity.status_text.setText(loginActivity.getResources().
                            getIdentifier("@string/error_in_pushing", "string", loginActivity.getPackageName()));
                    Log.d(DebugTag, "error in pushing to web server");
                }
            }
        }
        catch(Exception e){
            e.printStackTrace();
            Log.d(DebugTag, "Error due to no result: " + e.toString());
        }
    }
}









