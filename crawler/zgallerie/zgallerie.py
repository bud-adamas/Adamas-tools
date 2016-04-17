#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import urllib

# TODO(adamas): move it to a configuration file
images_path="images/"

root_url = 'http://www.zgallerie.com'

class ZgallerieSpider(scrapy.Spider):

    name = "zgallerie"

    def __init__(self):
        if not os.access(images_path, os.F_OK):
            os.mkdir(images_path)

        url_done = []

    start_urls = [
            "http://www.zgallerie.com/ViewAll.aspx?N=2000040",
                 ]

    def parse(self, response):
        image_list = response.xpath('//*[@id="myDiv"]/div/div/div[1]/a')

        for image in image_list:
            img_detail_url = image.xpath('@href').extract()[0]
            image_url = "http:" + image.xpath('img/@src').extract()[0]

            img_path = images_path + img_detail_url.split('.')[0] + "-s.jpg"
            urllib.urlretrieve(image_url, img_path)
            self.logger.info("Got " + image_url)

            dest_url = root_url + img_detail_url
            pic_id = 'ProductPic' + img_detail_url.split('.')[0].split('-')[1]

            self.logger.info("Go to " + dest_url)
            yield Request(dest_url, callback=self.parse_item)

    def parse_item(self, response):
        pic_id = 'ProductPic' + response.url.split('/')[-1].split('-')[1]
        image_url = response.xpath('//*[@id="' + pic_id + '"]/@src').extract()[0]

        image_name = image_url.split('/')[-1]
        img_path = images_path + image_name
        urllib.urlretrieve(image_url, img_path)
        self.logger.info("Got " + image_url)

        '''
response.xpath('//*[@id="HiddenProductDetails"]').extract()[0]

like:
<div id="HiddenProductDetails" border="0" width="100%" cellpadding="0" cellspacing="0" style="zoom: 1;visibility:hidden;"><div
id="galleryPopup" style="width: 0px; height:0px;border:1px solid #cccccc; cursor: pointer; position:
relative;padding-bottom:12px"><div id="apDiv5"><div id="izNav" style="position: relative; width: 100px; height:
100px;"></div></div><div id="izView" style="width: 817px; height: 475px; cursor: move; position: absolute;  left: 116px;
border-left:1px solid #cccccc;top:2px;text-align: center; z-index: 3;"> </div><script language="JavaScript"
type="text/javascript">var s7zoom=new SjZViewer(\'http://images.zgallerie.com/is/image/ZGallerie/\',\'730250472\', 817, 475,
\'3gEKcutzs1XImKMFnYJWly\');var s7navigator= new SjZoomNav(null, null, null, "relative");var zoomsteps = 2;var zoomlimit =
100;s7zoom.setBackground("0xffffff");s7zoom.initialRGNA("500,500,1100,1100");s7zoom.setBorder("0",
"#ccc");s7zoom.setFadeTime(.3);s7zoom.setMaxZoom(zoomlimit);s7zoom.setZoomStep(zoomsteps);s7zoom.setFormat("jpeg");if(S7ConfigClient.isVersion
== "2.7")s7zoom.setCachingModel("");s7zoom.addInformation("To Zoom click on the image.\\\\nTo Pan, click and hold the mouse while
dragging.");s7zoom.setHelpPage("www.scene7.com", "100,100");s7zoom.addToPage();s7navigator = new SjZoomNav(null, null, null,
"relative");s7navigator.setViewer(s7zoom.zviewer);s7navigator.visible(true);s7zoom.enableNav(0, 10, 466, 100,
100);s7zoom.setBorderNav(5, "#CCCCCC"); </script><div id="apDiv1"><div id="close1" onclick="galleryPopupClose()"></div></div><div
id="apDiv2"><div class="galleryThums"><div class="zoomPic"><table id="idzoomPictable" class="zoomPictable" cellpadding="0"
cellspacing="0" margin="0"> <tr><td><img src="images/zoom_01.jpg" width="20" height="22" valign="top" align="left"></td><td><a
href="javascript:s7zoom.zoomOut()"><img src="images/zoom_minus.jpg" name="btn_zoomout" valign="top" align="left" width="16"
height="22" onmouseover="chgImage(\'btn_zoomout\',\'zoomoutImg_on\')"
onmouseout="chgImage(\'btn_zoomout\',\'zoomoutImg_off\')"></a></td><td><img src="images/zoom_03.jpg" width="4" height="22"
align="left" valign="top"></td><td><a href="javascript:s7zoom.zoomIn();"><img src="images/zoom_plus.jpg" valign="top"
name="btn_zoomin" width="16" height="22" align="left" onmouseover="chgImage(\'btn_zoomin\',\'zoominImg_on\')"
onmouseout="chgImage(\'btn_zoomin\',\'zoominImg_off\')"></a></td><td><a href="javascript:s7zoom.zoomIn();"><img
src="images/zoom_05.jpg" width="48" height="22" align="left" valign="top"></a></td></tr></table></div><div
class="galleryThums2"><ul id="mycarousel" class="jcarousel-skin-tango"><li style="width:auto;border:none;"><a
href="javascript:changeImage(\'730250472\',\'http://images.zgallerie.com/is/image/ZGallerie\')"><img
src="http://images.zgallerie.com/is/image/ZGallerie/zoomthumb/space-between-730250472.jpg" width="68" height="68"
alt=""></a></li><li style="width:auto;border:none;"><a
href="javascript:changeImage(\'730250472_1\',\'http://images.zgallerie.com/is/image/ZGallerie\')"><img
src="http://images.zgallerie.com/is/image/ZGallerie/zoomthumb/space-between-730250472_1.jpg" width="68" height="68"
alt=""></a></li><li style="width:auto;border:none;"><a
href="javascript:changeImage(\'730250472_2\',\'http://images.zgallerie.com/is/image/ZGallerie\')"><img
src="http://images.zgallerie.com/is/image/ZGallerie/zoomthumb/space-between-730250472_2.jpg" width="68" height="68"
alt=""></a></li></ul></div></div></div></div></div>

get:
    var s7zoom=new SjZViewer(\'http://images.zgallerie.com/is/image/ZGallerie/\',\'730250472\', 817, 475,
    \'3gEKcutzs1XImKMFnYJWly\');

and the url is
    http://images.zgallerie.com/is/image/ZGallerie/730250472?rect=0,166,907,663&scl=2.315789473684211

All script:
    <script language="JavaScript" type="text/javascript">
    var s7zoom=new SjZViewer(\'http://images.zgallerie.com/is/image/ZGallerie/\',\'730250472\', 817, 475, \'3gEKcutzs1XImKMFnYJWly\');
    var s7navigator= new SjZoomNav(null, null, null, "relative");
    var zoomsteps = 2;
    var zoomlimit = 100;
    s7zoom.setBackground("0xffffff");
    s7zoom.initialRGNA("500,500,1100,1100");
    s7zoom.setBorder("0", "#ccc");
    s7zoom.setFadeTime(.3);
    s7zoom.setMaxZoom(zoomlimit);
    s7zoom.setZoomStep(zoomsteps);
    s7zoom.setFormat("jpeg");
    if(S7ConfigClient.isVersion == "2.7")s7zoom.setCachingModel("");
    s7zoom.addInformation("To Zoom click on the image.\\\\nTo Pan, click and hold the mouse while dragging.");
    s7zoom.setHelpPage("www.scene7.com", "100,100");
    s7zoom.addToPage();
    s7navigator = new SjZoomNav(null, null, null, "relative");
    s7navigator.setViewer(s7zoom.zviewer);
    s7navigator.visible(true);
    s7zoom.enableNav(0, 10, 466, 100, 100);
    s7zoom.setBorderNav(5, "#CCCCCC");
     </script>
        '''
