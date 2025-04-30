package cn.edu.siso.test.test.frags;

import android.view.View;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.os.Bundle;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.fragment.app.Fragment;

import cn.edu.siso.test.R;


public class NewsContentFragFragment extends Fragment {

    private LinearLayout visibilityLayout;
    private TextView title;
    private TextView content;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.news_content_frag, null);
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        visibilityLayout = (LinearLayout) view.findViewById(R.id.visibility_layout);
        title = (TextView) view.findViewById(R.id.title);
        content = (TextView) view.findViewById(R.id.content);

        visibilityLayout.setVisibility(View.VISIBLE);
    }

}
