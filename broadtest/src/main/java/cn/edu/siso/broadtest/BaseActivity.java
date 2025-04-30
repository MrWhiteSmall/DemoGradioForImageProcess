package cn.edu.siso.broadtest;

import android.app.Activity;
import android.content.IntentFilter;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class BaseActivity extends AppCompatActivity {
    ForceOfflineReceiver receiver;
    IntentFilter filter;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityController.addActivity(this);

    }

//    写在这里的注册和解注册 是为了只让栈顶的去接收这条广播，一旦不处于栈顶也就没必要去接收了
    @Override
    protected void onResume() {
        super.onResume();
        receiver = new ForceOfflineReceiver();
        filter = new IntentFilter("geiwoxiaxian");
        registerReceiver(receiver,filter);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (receiver!=null)
            unregisterReceiver(receiver);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        ActivityController.removeActivity(this);
    }
}
