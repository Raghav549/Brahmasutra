
package org.sutra.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        TextView tv = new TextView(this);

        tv.setText("नमस्ते — सूत्र अनुप्रयोगः");

        setContentView(tv);
    }
}
