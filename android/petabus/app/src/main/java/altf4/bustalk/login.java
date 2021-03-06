package altf4.bustalk;

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

import java.lang.String;

public class login extends AppCompatActivity {
    //declaration of variables
    public static final String DebugTag = "DEBUG_login";
    public static String PACKAGE_NAME;
    //private boolean flag1 = false, flag2 = false, flag3 = false;
    private String driver_id;
    private String password;
    private String ip_address;
    public login loginActivity;

    private EditText id_input;
    private EditText password_input;
    private EditText ip_address_input;
    public TextView status_text;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //set view upon entering this interface
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Log.d(DebugTag, "Creating interface");

        PACKAGE_NAME = getApplicationContext().getPackageName();
        //loginActivity = this;

        //map xml to java
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        id_input = findViewById(R.id.txtId);
        password_input = findViewById(R.id.txtPassword);
        ip_address_input = findViewById(R.id.txtIp);
        final Button login_button = findViewById(R.id.btnLogin);

        if(savedInstanceState == null) {
            Log.d(DebugTag, "Newly created");
        }

        /*
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
        });*/

        // when login button is clicked
        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d(DebugTag, "log in button pressed");

                // convert inputs to string
                driver_id = id_input.getText().toString();
                password = password_input.getText().toString();
                ip_address = ip_address_input.getText().toString();

                // hide ip address edit text upon logging in if it is visible
                if(ip_address_input.getVisibility() == View.VISIBLE){
                    ip_address_input.setVisibility(View.INVISIBLE);
                }

                // attempt to push only if both driver id and password are entered
                if((driver_id != "") && (password != "")){
                    // prepare the URL to push data to web server
                    String startURL = "http://" + ip_address + "/bustalk/verify.php";
                    String testURL = startURL + "?drvid=" + driver_id +
                            "&pw=" + password;
                    Log.d(DebugTag, "Send: " + testURL);

                    // push required information to the web server
                    networkManager netman = new networkManager(testURL, "GET", driver_id, ip_address);
                    netman.execute();
                }
                else{
                    // if driver id was not entered
                    if(driver_id == ""){
                        status_text.setText(getResources().getIdentifier("@string/no_bus_id", "string", PACKAGE_NAME));
                    }
                    else{
                        // if password was not entered
                        if(password == ""){
                            status_text.setText(getResources().getIdentifier("@string/no_bus_id", "string", PACKAGE_NAME));
                        }
                    }
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


/*
    public void nextActivity(String result) {
        Log.d(DebugTag, "Push status: " + result);

        // pass values to next activity and go to next activity if push was successful
        if(result.equals("0")){
            status_text.setText(getResources().getIdentifier("@string/login_attempt", "string", this.getPackageName()));
            //sendValuesToNextActivity();
            //proceedToSendLoc();
        }
        // otherwise error
        else{
            status_text.setText(getResources().getIdentifier("@string/error_in_pushing", "string", this.getPackageName()));
        }
    }

    // pass values in this activity to the next activity
    public void sendValuesToNextActivity(){
        Intent passIntent = new Intent(login.this, sendLoc.class);
        passIntent.putExtra("driver_id", driver_id);
        passIntent.putExtra("ip_address", ip_address);
        Log.d(DebugTag, "sending values to next activity");
        startActivity(passIntent);
    }

    // goes to next activity
    public void proceedToSendLoc() {
        Intent intent = new Intent(login.this, sendLoc.class);
        Log.d(DebugTag, "moving to next activity");
        startActivity(intent);
        this.finish();      // disable "back" to go back to login page
    }
    */
}

