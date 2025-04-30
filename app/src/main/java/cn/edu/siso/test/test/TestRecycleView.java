package cn.edu.siso.test.test;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.StaggeredGridLayoutManager;

import java.util.ArrayList;
import java.util.List;

import cn.edu.siso.test.R;

public class TestRecycleView extends BaseActivity {
    private RecyclerView recycleView;

    List<Fruit> fruits = new ArrayList<>();
    FruitAdapter adapter;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.recycle_test);
        int[] pic = {R.drawable.chun,R.drawable.qiu
                ,R.drawable.xia,R.drawable.dong,
                R.drawable.chun,R.drawable.qiu
                ,R.drawable.xia,R.drawable.dong};
        String[] texts = {getResources().getString(R.string.text1),
                getResources().getString(R.string.text2),
                getResources().getString(R.string.text3),
                getResources().getString(R.string.text4),
                getResources().getString(R.string.text1),
                getResources().getString(R.string.text2),
                getResources().getString(R.string.text3),
                getResources().getString(R.string.text4)};
        for (int i=0;i<pic.length;i++){
            Fruit fruit = new Fruit(pic[i],texts[i]);
            fruits.add(fruit);
        }
        adapter = new FruitAdapter();
        initView();

        recycleView.setAdapter(adapter);
    }

    private void initView() {
        recycleView = (RecyclerView) findViewById(R.id.recycleView);
//        linearLayoutManager gridLayoutManager StaggeredGridLayoutManger
//        LinearLayoutManager manager = new LinearLayoutManager(this);
//        manager.setOrientation(LinearLayoutManager.HORIZONTAL);
        StaggeredGridLayoutManager manager= new StaggeredGridLayoutManager(3
                ,StaggeredGridLayoutManager.VERTICAL);

        recycleView.setLayoutManager(manager);
    }

    class FruitAdapter extends RecyclerView.Adapter<FruitAdapter.ViewHolder>{

        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.fruit_item,null);
            ViewHolder holder = new ViewHolder(view);
            return holder;
        }

        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            Fruit fruit = fruits.get(position);
            holder.textView.setText(fruit.getText());
            holder.imageView.setImageResource(fruit.getPic());
        }

        @Override
        public int getItemCount() {
            return fruits.size();
        }

        class ViewHolder extends RecyclerView.ViewHolder{
            ImageView imageView;
            TextView textView;
            public ViewHolder(@NonNull View itemView) {
                super(itemView);
                imageView = itemView.findViewById(R.id.image);
                textView = itemView.findViewById(R.id.text);

            }
        }

    }
}



class Fruit{
    int pic;
    String text;

    public Fruit(int pic, String text) {
        this.pic = pic;
        this.text = text;
    }

    public int getPic() {
        return pic;
    }

    public void setPic(int pic) {
        this.pic = pic;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }
}
