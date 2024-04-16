package com.example.myapplication

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Find the WebView by its ID
        webView = findViewById(R.id.webView)

        // Enable JavaScript (optional, depending on your needs)
        val webSettings: WebSettings = webView.settings
        webSettings.javaScriptEnabled = true

        // Set a WebViewClient to handle events inside the WebView (e.g., clicks)
        webView.webViewClient = WebViewClient()

        // Load a URL into the WebView
//        webView.loadUrl("https://www.google.com")
        webView.loadUrl("file:///android_asset/template_files/index.html")
    }

    // Handle the back button to navigate within the WebView
    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
