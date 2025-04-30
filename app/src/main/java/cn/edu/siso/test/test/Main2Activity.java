package cn.edu.siso.test.test;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import cn.edu.siso.test.R;

public class Main2Activity extends BaseActivity implements View.OnClickListener {

    private Button back_result;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        initView();
    }

    public static void actionStart(Context context,String param1,String param2){
        Intent intent = new Intent(context,Main2Activity.class);
        intent.putExtra("param1",param1);
        intent.putExtra("param2",param2);
        context.startActivity(intent);

    }

    private void initView() {
        back_result = (Button) findViewById(R.id.back_result);

        back_result.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.back_result:
                Intent intent = new Intent();
                intent.putExtra("text","you are a pig");
                setResult(RESULT_OK,intent);
                finish();
                break;
        }
    }
}
