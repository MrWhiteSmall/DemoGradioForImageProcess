package cn.edu.siso.test.test;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import cn.edu.siso.test.R;

public class Test extends BaseActivity implements View.OnClickListener {
    //    logt 在onCreate方法外使自动生成 TAG
    private static final String TAG = "Test";
    private Button action_view;
    private Button action_dial;
    private Button for_result;

    double currentTime =0;
    int distance = 3000;


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
//        getActionBar().hide();
        initView();
        if (savedInstanceState!=null){
            Toast.makeText(this, savedInstanceState.getString("text")
                    , Toast.LENGTH_SHORT).show();
        }


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }

    @SuppressLint("WrongConstant")
    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case R.id.add:
                Toast.makeText(this, item.getTitle(), 2500).show();
                break;
            case R.id.remove:
                Toast.makeText(this, "remove one", 2500).show();
                break;
        }
        return true;
    }

    private void initView() {
        action_view = (Button) findViewById(R.id.action_view);
        action_dial = (Button) findViewById(R.id.action_dial);

        action_view.setOnClickListener(this);
        action_dial.setOnClickListener(this);
        for_result = (Button) findViewById(R.id.for_result);
        for_result.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.action_view:
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setData(Uri.parse("https://www.baidu.com"));
                startActivity(intent);
                break;
            case R.id.action_dial:
                Intent intent2 = new Intent(Intent.ACTION_DIAL);
                intent2.setData(Uri.parse("tel:10086"));
                startActivity(intent2);
                break;
            case R.id.for_result:
                Intent intent3 = new Intent(this,Main2Activity.class);
                startActivityForResult(intent3,1);
                break;
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode,
                                    @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
            case 1:
                if (resultCode==RESULT_OK){

                    String text = data.getStringExtra("text");
                    Toast.makeText(this,text,Toast.LENGTH_SHORT).show();
                }

                break;
        }
    }

    @Override
    protected void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putString("text","we are winner finally");
    }

    @Override
    public void onBackPressed() {
//        super.onBackPressed();
        if (System.currentTimeMillis()-currentTime>distance){
            currentTime = System.currentTimeMillis();
            Toast.makeText(this,"三秒内再次点击即可退出应用"
                    ,Toast.LENGTH_SHORT).show();
        }else {
            finish();
        }

    }

}
