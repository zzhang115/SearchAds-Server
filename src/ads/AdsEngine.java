package ads;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

/**
 * Created by zzc on 8/14/17.
 */
public class AdsEngine {
    private String mAdsDataFilePath;
    private String mBudgetFilePath;
    private IndexBuilder indexBuilder;
    private String mMemcachedServer;
    private int mMemcachedPortal;
    private String mysql_host;
    private String mysql_db;
    private String mysql_user;
    private String mysql_pass;

    public AdsEngine(String mAdsDataFilePath, String mBudgetFilePath, String mMemcachedServer, int mMemcachedPortal, String mysql_host, String mysql_db, String mysql_user, String mysql_pass) {
        this.mAdsDataFilePath = mAdsDataFilePath;
        this.mBudgetFilePath = mBudgetFilePath;
        this.mMemcachedServer = mMemcachedServer;
        this.mMemcachedPortal = mMemcachedPortal;
        this.mysql_host = mysql_host;
        this.mysql_db = mysql_db;
        this.mysql_user = mysql_user;
        this.mysql_pass = mysql_pass;
        indexBuilder = new IndexBuilder();
    }

    public boolean initEngine() {
        try {
            BufferedReader bufferedReader = new BufferedReader(new FileReader(mAdsDataFilePath));
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                JSONObject jsonObject = new JSONObject();
                if (jsonObject.isNull("adId") || jsonObject.isNull("campaignId")) {
                    continue;
                }
                long adId = jsonObject.getLong("adId");
                long campaignId = jsonObject.getLong("campaignId");
                String brand = jsonObject.isNull("brand") ? "" : jsonObject.getString("brand");
                String price = jsonObject.isNull("price") ? "" : jsonObject.getString("price");
                String thumbnail= jsonObject.isNull("thumbnail") ? "" : jsonObject.getString("thumbnail");
                String title = jsonObject.isNull("title") ? "" : jsonObject.getString("title");
                String detailUrl= jsonObject.isNull("detail_url") ? "" : jsonObject.getString("detail_url");
                String bidPrice = jsonObject.isNull("bidPrice") ? "" : jsonObject.getString("bidPrice");
                String pClick = jsonObject.isNull("pClick") ? "" : jsonObject.getString("pClick");
                String category = jsonObject.isNull("category") ? "" : jsonObject.getString("category");
                String description = jsonObject.isNull("description") ? "" : jsonObject.getString("description");
                String keyWords = jsonObject.isNull("keyWords") ? "" : jsonObject.getString("keyWords");
                List<String>
                Ad ad = new Ad()
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
