def downloadImage(query_string):
    from bing_image_downloader import downloader
    downloader.download(query_string.strip(), limit=1,  output_dir='viewListPage/assets/bingImages/', 
    adult_filter_off=True, force_replace=False, timeout=10, verbose=True)