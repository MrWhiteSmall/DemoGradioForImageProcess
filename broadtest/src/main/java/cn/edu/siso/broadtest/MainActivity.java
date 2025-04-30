package cn.edu.siso.broadtest;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends BaseActivity implements View.OnClickListener {

    private Button force_offline;


    public static void actionStart(Context context) {
        Intent intent = new Intent(context, MainActivity.class);
        context.startActivity(intent);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
    }

    private void initView() {
        force_offline = (Button) findViewById(R.id.force_offline);

        force_offline.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.force_offline:
                Intent intent = new Intent("geiwoxiaxian");
//                intent.setPackage(getPackageName());
                sendBroadcast(intent);
                break;
        }
    }
}
