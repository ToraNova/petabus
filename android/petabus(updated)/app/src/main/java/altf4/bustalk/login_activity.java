package altf4.bustalk;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Debug;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.lang.String;

public class login_activity extends AppCompatActivity {
    //declaration of variables
    public static final String DebugTag = "DEBUG_login";
    public static String PACKAGE_NAME;
    private String driver_id;
    private String password;
    private String ip_address;
    private Activity activity;

    private EditText id_input;
    private EditText password_input;
    private EditText ip_address_input;
    public TextView status_text;
    private networkManager netman;

    public static final String SHARED_PREF = "sharedPrefs";
    public static final String SAVED_DRIVER_ID = "id";
    public static final String SAVED_PASSWORD = "password";
    public static final String SAVED_IP = "ip";
    public static final String SAVED_STATE = "saved";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //set view upon entering this interface
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Log.d(DebugTag, "Creating interface");

        PACKAGE_NAME = getApplicationContext().getPackageName();
        activity = this;

        //map xml to java
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        id_input = findViewById(R.id.txtId);
        password_input = findViewById(R.id.txtPassword);
        ip_address_input = findViewById(R.id.txtIp);
        status_text = findViewById(R.id.txtStatus);
        final Button login_button = findViewById(R.id.btnLogin);

        if(savedInstanceState == null) {
            Log.d(DebugTag, "Newly created");
        }

        //loadData();

        // when login_activity button is clicked
        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d(DebugTag, "log in button pressed");

                // convert inputs to string
                driver_id = id_input.getText().toString();
                password = password_input.getText().toString();
                ip_address = ip_address_input.getText().toString();
                Log.d(DebugTag, "values: " + driver_id + "\t" + password);

                //saveData();

                // hide ip address edit text upon logging in if it is visible
                if(ip_address_input.getVisibility() == View.VISIBLE){
                    ip_address_input.setVisibility(View.INVISIBLE);
                }

                // attempt to push only if both driver id and password are entered
                if(driver_id.isEmpty() || password.isEmpty()) {
                    // if driver id was not entered
                    status_text.setVisibility(View.VISIBLE);
                    Log.d(DebugTag, "here");
                }
                else{
                    String startURL = "http://" + ip_address + ":8000/push/driver/login/valid";
                    String testURL = startURL + "?f0=" + driver_id +
                            "&f1=" + password;
                    String parameters = "f0=" + driver_id +
                            "&f1=" + password;
                    Log.d(DebugTag, "Send: " + testURL);

                    // push required information to the web server
                    netman = new networkManager(activity);
                    netman.setDriverId(driver_id);
                    netman.setIp(ip_address);
                    netman.setParam(parameters);
                    netman.setUrlMini(startURL);
                    netman.setType("GET");
                    netman.setUrlString(testURL);
                    netman.execute();
                }
            }
        });
        Log.d(DebugTag, "on create completed");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.login_option, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // action bar will automatically handle clicks on top toolbar
        int id = item.getItemId();

        if (id == R.id.action_ip) {
            // toggle visibility of ip address edit text upon clicking
            if(ip_address_input.getVisibility() == View.INVISIBLE) {
                Log.d(DebugTag, "IP Address edit text invisible, make it visible");
                ip_address_input.setVisibility(View.VISIBLE);
            }
            else{
                Log.d(DebugTag, "IP Address edit text visible, make it invisible");
                ip_address_input.setVisibility(View.INVISIBLE);
            }
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void saveData(){
        // no other app can change the shared prefs
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        //editor.putString(SAVED_DRIVER_ID, driver_id);
        //editor.putString(SAVED_PASSWORD, password);
        editor.putString(SAVED_IP, ip_address);
        editor.apply();

        Toast.makeText(this, "Data Saved", Toast.LENGTH_SHORT).show();
        Log.d(DebugTag, "id: " + driver_id + ", pw: " + password + ", ip: " + ip_address);
    }

    public void loadData(){
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF, MODE_PRIVATE);

        /*
        id_input.setText(sharedPreferences.getString(SAVED_DRIVER_ID, ""));
        //password_input.setText(sharedPreferences.getString(SAVED_PASSWORD, ""));
        */
        ip_address_input.setText(sharedPreferences.getString(SAVED_IP, ""));

        /*
        StringBuilder str = new StringBuilder();
        if (sharedPreferences.contains(SAVED_DRIVER_ID)) {
            id_input.setText(sharedPreferences.getString(SAVED_DRIVER_ID, ""));
        }
        if (sharedPreferences.contains(SAVED_IP)) {
            id_input.setText(sharedPreferences.getString(SAVED_IP, "192.168.1.100"));
        }*/

        Toast.makeText(this, "Data Loaded", Toast.LENGTH_SHORT).show();
    }
}

