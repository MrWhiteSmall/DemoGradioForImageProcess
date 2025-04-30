package cn.edu.siso.test.test.frags;

import android.view.View;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.os.Bundle;
import android.widget.Button;

import androidx.fragment.app.Fragment;

import cn.edu.siso.test.R;

public class LeftFragFragment extends Fragment implements View.OnClickListener {


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.left_frag, null);
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        view.findViewById(R.id.button).setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.button:
                //TODO implement
                replaceFrag(new RightFrag2Fragment());
                break;
        }
    }

    void replaceFrag(Fragment fragment){
        getFragmentManager().beginTransaction()
                .replace(R.id.right_frag,fragment)
                .addToBackStack(null)
                .commit();
    }
}
