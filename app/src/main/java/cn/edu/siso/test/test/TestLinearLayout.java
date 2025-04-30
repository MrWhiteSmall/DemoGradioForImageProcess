package cn.edu.siso.test.test;

import android.app.Activity;
import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Toast;

import androidx.annotation.Nullable;

import cn.edu.siso.test.R;

public class TestLinearLayout extends LinearLayout {

    private Button back;
    private Button edit;

    public TestLinearLayout(final Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        LayoutInflater.from(context).inflate(R.layout.top_title, this);
        back= findViewById(R.id.back);
        edit= findViewById(R.id.edit);
        back.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                ((Activity)getContext()).finish();
            }
        });
        edit.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getContext(),"you c" +
                        "lick a button",Toast.LENGTH_SHORT).show();
            }
        });
    }
}
