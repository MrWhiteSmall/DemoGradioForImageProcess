package cn.edu.siso.test.test;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

import cn.edu.siso.test.R;
import cn.edu.siso.test.test.adapters.MyAdapter;
import cn.edu.siso.test.test.beans.Msg;

public class TestRecycleView2 extends BaseActivity implements View.OnClickListener {
    private RecyclerView recycleView;
    private EditText input_text;
    private Button send;

    List<Msg> list = new ArrayList<>();
    MyAdapter adapter;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.recycle_test2);
        Msg msg = new Msg("hello",Msg.TYPE_RECEIVED);
        Msg msg2 = new Msg("no ok",Msg.TYPE_SENT);
        Msg msg3 = new Msg("???",Msg.TYPE_RECEIVED);
        list.add(msg);
        list.add(msg2);
        list.add(msg3);
        initView();


    }

    private void initView() {
        recycleView = (RecyclerView) findViewById(R.id.recycleView);
        input_text = (EditText) findViewById(R.id.input_text);
        send = (Button) findViewById(R.id.send);

        LinearLayoutManager manager = new LinearLayoutManager(this);
//        manager.setOrientation(RecyclerView.HORIZONTAL);
        recycleView.setLayoutManager(manager);
        adapter = new MyAdapter(list);
        recycleView.setAdapter(adapter);

        send.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.send:
                submit();
                break;
        }
    }

    private void submit() {
        // validate
        String text = input_text.getText().toString().trim();
        if (TextUtils.isEmpty(text)) {
            Toast.makeText(this, "type something here", Toast.LENGTH_SHORT).show();
            return;
        }

        Msg msg = new Msg(text,Msg.TYPE_SENT);
        list.add(msg);
        adapter.notifyItemInserted(list.size()-1);
//        adapter.notifyDataSetChanged();
        recycleView.scrollToPosition(list.size()-1);
        input_text.setText("");
        // TODO validate success, do something

        receiver();
    }

    void receiver(){
        Msg msg = new Msg("i get it ok ok oko okodsahdkajhdjahdajs",Msg.TYPE_RECEIVED);
        list.add(msg);
        adapter.notifyItemInserted(list.size()-1);
//        adapter.notifyDataSetChanged();
        recycleView.scrollToPosition(list.size()-1);
//        input_text.setText("");
    }
}
