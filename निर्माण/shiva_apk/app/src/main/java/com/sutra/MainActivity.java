
package com.sutra;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;

public class MainActivity extends Activity {

    public void onCreate(Bundle b){
        super.onCreate(b);

        WebView w = new WebView(this);

        w.loadUrl("file:///android_asset/index.html");

        setContentView(w);
    }

}
