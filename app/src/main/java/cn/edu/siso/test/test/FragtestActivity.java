package cn.edu.siso.test.test;

import android.app.Activity;
import android.os.Bundle;
import android.widget.FrameLayout;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import cn.edu.siso.test.R;
import cn.edu.siso.test.test.frags.LeftFragFragment;
import cn.edu.siso.test.test.frags.RightFragFragment;

public class FragtestActivity extends AppCompatActivity {


    private FrameLayout left_frag;
    private FrameLayout right_frag;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragtest);
        initView();

    }

    private void initView() {
        left_frag = (FrameLayout) findViewById(R.id.left_frag);
        right_frag = (FrameLayout) findViewById(R.id.right_frag);
        replaceLeftFrag(new LeftFragFragment());
        replaceRightFrag(new RightFragFragment());
    }

    void replaceLeftFrag(Fragment fragment){
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.left_frag,fragment)
                .commit();
    }
    void replaceRightFrag(Fragment fragment){
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.right_frag,fragment)
                .commit();
    }
}
