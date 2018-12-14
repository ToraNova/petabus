package altf4.bustalk;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.lang.String;

//custom imports

public class login extends AppCompatActivity {
    //declaration of variables
    public static final String DebugTag = "DEV_LOGIN_DEBUG_MSG";
    private boolean flag1 = false, flag2 = false, flag3 = false;
    private String driver_id;
    private String bus_number;
    private String ip_address;

    private EditText id_input;
    private EditText bus_number_input;
    private EditText ip_address_input;
    private TextView status_text;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //set view upon entering this interface
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //map xml to java
        id_input = findViewById(R.id.txtDriverId);
        bus_number_input = findViewById(R.id.txtBusNumber);
        ip_address_input = findViewById(R.id.txtIP);
        status_text = findViewById(R.id.lblLogInStatus);
        final Button login_button = findViewById(R.id.btnLogIn);

        id_input.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {
            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
            }

            @Override
            public void afterTextChanged(Editable editable) {
                //validate input
                int n = editable.toString().length();
                if (n < 10 ) {
                    id_input.setError("Invalid driver ID");
                    flag1 = false;
                } else{
                    flag1 = true;
                }
            }
        });
        bus_number_input.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) { }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) { }

            @Override
            public void afterTextChanged(Editable editable) {
                //validate input
                int n = editable.toString().length();
                if (n < 4 ) {
                    bus_number_input.setError("Invalid bus number");
                    flag2 = false;
                } else{
                    flag2 = true;
                }
            }
        });
        ip_address_input.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) { }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) { }

            @Override
            public void afterTextChanged(Editable editable) {
                //validate input
                int n = editable.toString().length();
                if (n < 7 ) {
                    ip_address_input.setError("Invalid IP address");
                    flag3 = false;
                } else{
                    flag3 = true;
                }
            }
        });

        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //when login button is clicked
                Log.d(DebugTag, "log in button pressed");
                status_text.setText("Attempt to log in");
                if (flag1 && flag2 && flag3){
                    //convert inputs to string
                    driver_id = id_input.getText().toString();
                    bus_number = bus_number_input.getText().toString();
                    ip_address = ip_address_input.getText().toString();

                    //prepare the URL to push data to web server
                    String startURL = "http://" + ip_address + "/bustalk/verify.php";
                    String testURL = startURL + "?drvid=" + driver_id +
                            "&busid=" + bus_number;

                    //push required information to the web server
                    new NetworkManager().execute(testURL);
                }
            }
        });
        Log.d(DebugTag, "on create completed");
    }

    //goes to next activity
    public void login2push() {
        Intent intent = new Intent(this, push.class);
        startActivity(intent);
    }

    //pass values in this activity to the next activity
    public void sendValuesToNextActivity(){
        Intent passIntent = new Intent(login.this, push.class);
        passIntent.putExtra("driver_id", driver_id);
        passIntent.putExtra("bus_number", bus_number);
        passIntent.putExtra("ip_address", ip_address);
        startActivity(passIntent);
    }

    //HTTP GET function
    class NetworkManager extends AsyncTask<String, Void, String> {
        protected String doInBackground(String... strings) {
            //declare and initialise
            String buffer = "";
            String urlString = strings[0];
            URL url;
            HttpURLConnection connection = null;
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
                    buffer += current;
                }
                Log.d(DebugTag, buffer);

            } catch (Exception e) {
                // Writing exception to log
                e.printStackTrace();
                Log.d(DebugTag, "Error in pushing location data:   " + e.toString());
            } finally {
                if (connection != null) {
                    connection.disconnect();
                }
            }
            return buffer;
        }

        protected void onPostExecute(String result) {
            //showDialog("Downloaded " + result + " bytes");
            Log.d(DebugTag, "Push status: " + result);

            if(result.equals("0")){
                //pass values to next activity and go to next activity if push was successful
                sendValuesToNextActivity();
                login2push();
            }
            else{
                //otherwise display error message on screen
                status_text.setText("Error in pushing data to web server");
            }
        }
    }
}

