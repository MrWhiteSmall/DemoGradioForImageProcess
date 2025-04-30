package cn.edu.siso.test.test;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import cn.edu.siso.test.R;

public class BoradcastTest extends AppCompatActivity implements View.OnClickListener {
    MyReceiver receiver;
    private Button send;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_boradcast_test);
        requestPermissions(new String[]{Manifest.permission.RECEIVE_BOOT_COMPLETED}
        ,1);
        initView();
        receiver = new MyReceiver();
        IntentFilter filter = new IntentFilter("android.net.conn.CONNECTIVITY_CHANGE");
        registerReceiver(receiver, filter);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }

    private void initView() {
        send = (Button) findViewById(R.id.send);

        send.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.send:
                Intent intent = new Intent(
                        "android.intent.action.MyBroad");
                intent.setPackage(getPackageName());
                sendBroadcast(intent);
                break;
        }
    }

    class MyReceiver extends BroadcastReceiver {

        @Override
        public void onReceive(Context context, Intent intent) {

            ConnectivityManager manager = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
            NetworkInfo networkInfo = manager.getActiveNetworkInfo();
            if (networkInfo != null && networkInfo.isAvailable()) {
                switch (networkInfo.getType()) {
                    case ConnectivityManager.TYPE_WIFI:
                        Toast.makeText(context, networkInfo.getTypeName()
                                , Toast.LENGTH_SHORT).show();
                        break;
                    case ConnectivityManager.TYPE_MOBILE:
                        Toast.makeText(context, "this net is 4G "
                                , Toast.LENGTH_SHORT).show();
                        break;
                }
            }

        }
    }
}
