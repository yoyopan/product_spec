目前版本尚未提供上傳功能，product_spec.js會產生在當前目錄下


products:
	依照產品名稱(可縮寫)建立對應資料夾，資料夾內依據Video Format建立資料夾(Ex: H.264)
	
	舉例
	products下建立Mainconsole NH-4500資料夾，裡面分別放了Mainconsole NH-4500.json以及H.264資料夾。
	Mainconsole NH-4500.json是設定檔不需修改
	H.264資料夾內放了config.json，以及1.csv, 2.csv, 3.csv(絕對限制以單一數字命名，順序很重要)
	
	在config.json當中設定video_format欄位為H.264，並指定每一個係數要從哪一張數據表取得，
	例如local_display_rf要從數據表1取得，ivs_p要從第3張表取得
	
	欄位對應說明
        "local_display_rf":  	// Local Display(Resolution * FPS)
        "local_display_b":  	// Local Display(Bit rate)
        "smart_guard_rf":  		// Smart Guard or Motion Analysis (Resolution * FPS)
        "smart_guard_b":  		// Smart Guard or Motion Analysis (Bit rate)
        "smart_guard_p":  		// Smart Guard or Motion Analysis (Pure analysis)
        "ivs_rf":  				// IVS (Resolution * FPS)
        "ivs_b":  				// IVS (Bit rate)
        "ivs_p":  				// IVS (Pure analysis)
        "live_view":  			// Live View Connection (Bit rate)
        "record":  				// Record (Bit rate)
        "metadata":  			// Metadata
        "edge_event": 			// Edge Event
		
		
	csv數據表只限英數字，欄位header不允許換行與特殊符號，各欄位名稱不可修改
	數據表新增一欄位const，內容一律為0(常數為0的意思)
	欄位命名規則: 所有單字都大寫開頭，單字之間一個空白，在盡量遵循QA的命名規則下新增一些關鍵字
	Ex: (Pure)，const等等
	
cameras:
	目前不須更動

client_pc:
	目前不須更動