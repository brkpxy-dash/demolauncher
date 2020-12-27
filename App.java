package live.wick3d.democlient;

import static javax.swing.JOptionPane.showMessageDialog;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class App 
{
    public static void main( String[] args ) throws Exception
    {
    	String jsonID = getIDfromJSON();
    	if (args.length == 1) {
    		String ID = args[0];
        	if (ID.equals(jsonID) && activateSession(ID).equals("OK")) {
            	showMessageDialog(null, "Session is valid and was made active. Pretend this is the game.");
        	} else {
        		invalidate();
        	}
    	} else {
    		invalidate();
    	}
    	
    }
    
    public static void invalidate()
    {
    	showMessageDialog(null, "Session invalid!");
    }
    
    public static String getIDfromJSON() throws Exception
    {
    	JSONObject jsonObject = (JSONObject) readJsonSimpleDemo("/sessionID.json");
    	return jsonObject.get("sessionID").toString();
    }
    
    public static Object readJsonSimpleDemo(String filename) throws Exception {
    	InputStream in = App.class.getResourceAsStream(filename); 
    	BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        JSONParser jsonParser = new JSONParser();
        return jsonParser.parse(reader);
    }
    
    public static String activateSession(String ID) throws Exception
    {
    	String returnString = "";
    	HttpClient httpClient = HttpClientBuilder.create().build();
    	try {
    	    HttpPost request = new HttpPost("http://localhost:5000/instance");
    	    List<NameValuePair> params = new ArrayList<>();
            params.add(new BasicNameValuePair("id", ID));
    	    request.setEntity(new UrlEncodedFormEntity(params));
    	    HttpResponse response = httpClient.execute(request);
    	    HttpEntity responseEntity = response.getEntity();
    	    returnString = EntityUtils.toString(responseEntity);
    	} catch (Exception ex) {
    	} finally {
    	}
		return returnString;
    }
    
}
