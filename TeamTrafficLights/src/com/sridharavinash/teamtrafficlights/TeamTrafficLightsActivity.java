package com.sridharavinash.teamtrafficlights;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Iterator;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.apache.http.HttpHost;
import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.AbstractHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;



public class TeamTrafficLightsActivity extends Activity {
	// Button Listener
	private OnClickListener connectListener = new OnClickListener(){
		public void onClick(View v){
			InputMethodManager imm = (InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE);
			imm.hideSoftInputFromWindow(v.getWindowToken(), 0);

			//Get user input data
			EditText teamCityUrl = (EditText)findViewById(R.id.serverUrl);
			EditText teamCityUser = (EditText)findViewById(R.id.user);
			EditText teamCityPass = (EditText)findViewById(R.id.pass);
			
			getResponse(teamCityUrl.getText().toString().trim(),teamCityUser.getText().toString().trim(),teamCityPass.getText().toString());
		}
	};
	
	/** Convenience function to convert inputstream(like HttpResponse) to a string */
	private StringBuilder inputStreamToString(InputStream is) {
	    String line = "";
	    StringBuilder total = new StringBuilder();
	    
	    // Wrap a BufferedReader around the InputStream
	    BufferedReader rd = new BufferedReader(new InputStreamReader(is));

	    // Read response until the end
	    try {
			while ((line = rd.readLine()) != null) { 
			    total.append(line); 
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	    
	    // Return full string
	    return total;
	}

	/**Make a call to the server with credentials and get a response */
	private void getResponse(String url, String user, String pass){
		HttpHost targetHost = new HttpHost(url, 80, "http");
		
		HttpClient httpClient = new DefaultHttpClient();
		
		((AbstractHttpClient) httpClient).getCredentialsProvider().setCredentials(
				new AuthScope(targetHost.getHostName(),targetHost.getPort()), 
				new UsernamePasswordCredentials(user,pass));
		
		
		HttpGet httpGet = new HttpGet("http://"+url+"/httpAuth/app/rest/projects");
		HttpResponse httpResponse;
		try{
			httpResponse = httpClient.execute(httpGet);
			StringBuilder resp = inputStreamToString(httpResponse.getEntity().getContent());
			ArrayList<TeamCityProject> projectList = ParseXMLResponse(resp);
			showProjectList(projectList);
		}catch (ClientProtocolException e){
			e.printStackTrace();
		    AlertDialog alertDialog = new AlertDialog.Builder(TeamTrafficLightsActivity.this).create();
		    alertDialog.setTitle("Erorr");
		    alertDialog.setMessage("Oh Oh! We are having trouble connecting to the server with those credentials! Please recheck your url, username and password.");
		    alertDialog.show();
		} catch (IOException e) {
			e.printStackTrace();
			AlertDialog alertDialog = new AlertDialog.Builder(TeamTrafficLightsActivity.this).create();
		    alertDialog.setTitle("Erorr");
		    alertDialog.setMessage("Oh Oh! We are having trouble connecting to the server with those credentials!Please recheck your url, username and password.");
		    alertDialog.show();
		}
	}
	
	/** Show a list of projects from server */
	private void showProjectList(ArrayList<TeamCityProject> projectList){
		ArrayList<String> myList = new ArrayList<String>();
		Iterator<TeamCityProject> iterator = projectList.iterator();
		while(iterator.hasNext()){
			myList.add(iterator.next().projectName);
		}
		if(myList.isEmpty())
			myList.add("No Projects!");
        ListView lv = new ListView(this);
        lv.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,myList));
        setContentView(lv);
	}

	/** Parse response to get a list of available projects from the server
	 * @return */
	private ArrayList<TeamCityProject> ParseXMLResponse(StringBuilder response){
		 SAXParserFactory spf = SAXParserFactory.newInstance();
		 TCDataHandler myHandler = new TCDataHandler();
		 try {
			SAXParser sp = spf.newSAXParser();
			XMLReader xr = sp.getXMLReader();
			
			xr.setContentHandler(myHandler);
			InputSource is = new InputSource();
			is.setCharacterStream(new StringReader(response.toString()));
			xr.parse(is);
			
		} catch (ParserConfigurationException e) {
			e.printStackTrace();
		} catch (SAXException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return myHandler.getProjects();
	}
	
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        Button connect = (Button)findViewById(R.id.Connect);
        connect.setOnClickListener(connectListener);
    }
}