package cn.edu.siso.filetest;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import org.litepal.LitePal;
import org.litepal.tablemanager.Connector;

import java.util.List;

public class LitePalTest extends AppCompatActivity implements View.OnClickListener {

    private Button create_db;
    private Button insert_data;
    private Button delete_date;
    private Button update_db;
    private Button query_data;

    private static final String TAG = "LitePalTest";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lite_pal_test);
        LitePal.initialize(this);
        initView();

    }

    private void initView() {
        create_db = (Button) findViewById(R.id.create_db);

        create_db.setOnClickListener(this);
        insert_data = (Button) findViewById(R.id.insert_data);
        insert_data.setOnClickListener(this);
        delete_date = (Button) findViewById(R.id.delete_date);
        delete_date.setOnClickListener(this);
        update_db = (Button) findViewById(R.id.update_db);
        update_db.setOnClickListener(this);
        query_data = (Button) findViewById(R.id.query_data);
        query_data.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.create_db:
                Connector.getDatabase();
                Log.e(TAG, "create table success ");
                break;
            case R.id.insert_data:
                for (int i=0;i<5;i++){
                    Book book = new Book();
                    book.setId(i+1);
                    book.setAuthor("hulala");
                    book.setPress("中国");
                    book.setName("wang");
                    book.setPrice(Math.random()*50);
                    book.setPages((int)(Math.random()*100));
                    book.save();
                }
                Log.e(TAG, "insert: "+ LitePal.findAll(Book.class).size());
                break;
            case R.id.delete_date:
                LitePal.deleteAll(Book.class,"price<?","20");
                Log.e(TAG, "delete: "+ LitePal.findAll(Book.class).size());
                break;
            case R.id.update_db:
                Book book = new Book() ;
                book.setPress("美国");
                book.setName("汪峰");
                book.updateAll("price>?","30");
                Log.e(TAG, "update: "+ LitePal.findAll(Book.class).size());
                break;
            case R.id.query_data:
                List<Book> books = LitePal.findAll(Book.class);
                StringBuilder builder = new StringBuilder();
                for (Book b : books){
                    builder.append(b.getId()+":"+
                            b.getAuthor()+":"+
                            b.getName()+":"+
                            b.getPages()+":"+
                            b.getPrice()+":"+
                            b.getPress()+":"+
                            "\n");
                }
                Log.e(TAG, "query: "+ builder.toString());
                break;
        }
    }
}
