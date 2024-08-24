package com.opengms.sabackproject.utils;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

public class Utils {

    public static JSONObject convertMdl(String mdl) {
        JSONObject mdlObj = new JSONObject();
        try {
            Document mdlDoc = DocumentHelper.parseText(mdl);
            Element rootElement = mdlDoc.getRootElement();
            mdlObj.put("name", rootElement.attributeValue("name"));


            Element AttributeSet = rootElement.element("AttributeSet");
            Element Behavior = rootElement.element("Behavior");

            //基本属性开始
            Element Category = AttributeSet.element("Categories").element("Category");
            mdlObj.put("principle", Category.attributeValue("principle"));
            mdlObj.put("path", Category.attributeValue("path"));

            List<Element> LocalAttributes = AttributeSet.element("LocalAttributes").elements();
            if (LocalAttributes.size() > 0) {
                for (Element LocalAttribute : LocalAttributes) {
                    JSONObject local = new JSONObject();
                    local.put("localName", LocalAttribute.attributeValue("localName"));
                    Element Keywords = LocalAttribute.element("Keywords");
                    local.put("keywords", Keywords.getText());
                    Element Abstract = LocalAttribute.element("Abstract");
                    local.put("abstract", Abstract.getText());
                    if (LocalAttribute.attributeValue("local").equals("EN_US")) {
                        mdlObj.put("enAttr", local);
                    } else {
                        mdlObj.put("cnAttr", local);
                    }
                }
            }
            //基本属性结束

            //相关数据开始


            Element RelatedDatasets = Behavior.element("RelatedDatasets");
            if (RelatedDatasets == null) {
                RelatedDatasets = Behavior.element("DatasetDeclarations");
            }
            List<Element> DatasetItems = RelatedDatasets.elements();
            if (DatasetItems.size() > 0) {
                String relatedDatasets = mdl.substring(mdl.indexOf("<RelatedDatasets>") + 17, mdl.indexOf("</RelatedDatasets>"));
                JSONArray DatasetItemArray = new JSONArray();
                for (Element DatasetDeclaration : DatasetItems) {
                    JSONArray dataset = new JSONArray();
                    JSONObject root = new JSONObject();
                    root.put("text", DatasetDeclaration.attributeValue("name"));
                    if (DatasetDeclaration.attribute("description") != null) {
                        root.put("desc", DatasetDeclaration.attributeValue("description"));
                    } else {
                        root.put("desc", "");
                    }
                    root.put("dataType", DatasetDeclaration.attributeValue("type"));
                    if (DatasetDeclaration.attributeValue("type").equals("external")) {
                        String external = "";
                        if (DatasetDeclaration.attribute("externalId") != null) {
                            external = DatasetDeclaration.attributeValue("externalId");
                        } else if (DatasetDeclaration.attribute("external") != null) {
                            external = DatasetDeclaration.attributeValue("external");
                        }
                        root.put("externalId", external.toLowerCase());

                        root.put("parentId", "null");
                        dataset.add(root);
                    } else {
                        Element UDXDeclaration;
                        if (DatasetDeclaration.element("UdxDeclaration") != null) {
                            UDXDeclaration = DatasetDeclaration.element("UdxDeclaration");
                        } else {
                            UDXDeclaration = DatasetDeclaration.element("UDXDeclaration");
                        }
                        String rootId = "";
                        if (UDXDeclaration.attribute("id") != null) {
                            rootId = "root" + UDXDeclaration.attributeValue("id");
                        } else {
                            rootId = "root" + UUID.randomUUID().toString();
                        }
                        root.put("Id", rootId);
                        root.put("parentId", "null");

                        Element udxNode;
                        if (UDXDeclaration.element("UDXNode") != null) {
                            udxNode = UDXDeclaration.element("UDXNode");
                        } else {
                            udxNode = UDXDeclaration.element("UdxNode");
                        }
                        List<Element> UdxNodes = udxNode.elements();
                        if (UdxNodes.size() > 0) {
                            root.put("schema",Utils.getUdxSchema(relatedDatasets,root.getString("text")));
                            root.put("nodes", new JSONArray());
                            convertData(UdxNodes, root);
                        }
                        dataset.add(root);
                    }
                    DatasetItemArray.add(dataset);
                }
                mdlObj.put("DataItems", DatasetItemArray);
            }
            //相关数据结束

            //State开始
            Element States = Behavior.element("StateGroup").element("States");
            List<Element> StateList = States.elements();
            JSONArray states = new JSONArray();
            if (StateList.size() > 0) {
                for (Element State : StateList) {
                    JSONObject stateObj = new JSONObject();
                    stateObj.put("name", State.attributeValue("name"));
                    stateObj.put("type", State.attributeValue("type"));
                    stateObj.put("desc", State.attributeValue("description"));
                    stateObj.put("Id", State.attributeValue("id"));
                    List<Element> EventList = State.elements();
                    JSONArray event = new JSONArray();
                    for (Element Event : EventList) {
                        JSONObject eventObj = new JSONObject();
                        eventObj.put("eventId", UUID.randomUUID().toString());
                        eventObj.put("eventName", Event.attributeValue("name"));
                        eventObj.put("eventType", Event.attributeValue("type"));
                        eventObj.put("eventDesc", Event.attributeValue("description"));
                        Element Parameter = null;
                        if (Event.attributeValue("type").equals("response")) {
                            Parameter = Event.element("ResponseParameter");
                            if (Event.attribute("optional") != null) {
                                if (Event.attributeValue("optional").equalsIgnoreCase("True")) {
                                    if (Event.element("ControlParameter") != null) {
                                        Parameter = Event.element("ControlParameter");
                                    }
                                    eventObj.put("optional", true);
                                } else {
                                    eventObj.put("optional", false);
                                }
                            }
                        } else {
                            Parameter = Event.element("DispatchParameter");
                            if (Event.attribute("optional") != null) {
                                if (Event.attributeValue("optional").equalsIgnoreCase("True")) {
                                    if (Event.element("ControlParameter") != null) {
                                        Parameter = Event.element("ControlParameter");
                                    }
                                    eventObj.put("optional", true);
                                } else {
                                    eventObj.put("optional", false);
                                }
                            }
                            if(Event.attribute("multiple") != null){//判断是否可以多输出
                                if(Event.attributeValue("multiple").equalsIgnoreCase("True")){
                                    eventObj.put("multiple", true);

                                }else{
                                    eventObj.put("multiple", false);
                                }
                            }
                        }

                        for (int i = 0; i < mdlObj.getJSONArray("DataItems").size(); i++) {
                            JSONArray currentDataSet = mdlObj.getJSONArray("DataItems").getJSONArray(i);
                            JSONObject rootData = currentDataSet.getJSONObject(0);
                            if (Parameter == null) {
                                break;
                            }
                            if (rootData.getString("text").equals(Parameter.attributeValue("datasetReference"))) {
                                eventObj.put("data", currentDataSet);
                            }
                        }
                        event.add(eventObj);
                    }
                    stateObj.put("event", event);
                    states.add(stateObj);
                }
            }
            mdlObj.put("states", states);
            //State结束
        } catch (DocumentException e) {
            System.out.println(mdl);
            e.printStackTrace();
        }
        JSONObject result = new JSONObject();
        result.put("mdl", mdlObj);
        return result;
    }

    public static void convertData(List<Element> udxNodes, JSONObject root) {
        if (udxNodes.size() > 0) {
            for (Element udxNode : udxNodes) {
                JSONObject node = new JSONObject();
                node.put("text", udxNode.attributeValue("name"));
                String dataType=udxNode.attributeValue("type");
                String dataType_result="";
                String[] dataTypes=dataType.split("\\|");
                if(dataTypes.length>1){
                    for(int j=0;j<dataTypes.length;j++){
                        String[] strings=dataTypes[j].trim().split("_");
                        if(strings[1].equals("LIST")){
                            strings[1]="ARRAY";
                        }
                        dataType_result+=strings[1];
                        if(j!=dataTypes.length-1){
                            dataType_result+="_";
                        }
                    }
                }
                else{
                    String[] strings=dataType.split("_");
                    dataType_result=strings[1];
                }

                node.put("dataType", dataType_result);
                node.put("desc", udxNode.attributeValue("description"));
                if (udxNode.attributeValue("type").equals("external")) {
                    node.put("externalId", udxNode.attributeValue("externalId").toLowerCase());
                }
                List<Element> nodeChildren = udxNode.elements();
                if (nodeChildren.size() > 0) {
                    node.put("nodes", new JSONArray());
                    convertData(nodeChildren, node);
                }
                JSONArray nodes = root.getJSONArray("nodes");
                nodes.add(node);
            }
        } else {
            return;
        }
    }

    public static String getUdxSchema(String text,String name){
        int findIndex=text.indexOf(name);
        int startIndex=text.indexOf(">",findIndex+name.length())+1;
        int endIndex=text.indexOf("</DatasetItem>",startIndex);
        return text.substring(startIndex,endIndex);
    }

    public static JSONObject postJSON(String urlStr, JSONObject jsonParam) {
        try {

            //System.out.println(obj);
            // 创建url资源
            URL url = new URL(urlStr);
            // 建立http连接
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            // 设置允许输出
            conn.setDoOutput(true);

            conn.setDoInput(true);

            // 设置不用缓存
            conn.setUseCaches(false);
            // 设置传递方式
            conn.setRequestMethod("POST");
            // 设置维持长连接
            conn.setRequestProperty("Connection", "Keep-Alive");
            // 设置文件字符集:
            conn.setRequestProperty("Charset", "UTF-8");
            //转换为字节数组
            byte[] data = (jsonParam.toJSONString()).getBytes();

            // 设置文件长度
            conn.setRequestProperty("Content-Length", String.valueOf(data.length));

            // 设置文件类型:
            conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");


            // 开始连接请求
            conn.connect();
            OutputStream out = conn.getOutputStream();
            // 写入请求的字符串
            out.write(data);
            out.flush();
            out.close();

            System.out.println(conn.getResponseCode());
            System.out.println(conn.getResponseMessage());

            // 请求返回的状态
            if (conn.getResponseCode() == 200) {
                System.out.println("连接成功");
                // 请求返回的数据
                InputStream in = conn.getInputStream();
                String a = null;
                try {
                    byte[] data1 = new byte[in.available()];
                    in.read(data1);
                    // 转成字符串
                    a = new String(data1);
                    System.out.println(a);
                    return JSONObject.parseObject(a);
                } catch (Exception e1) {
                    // TODO Auto-generated catch block
                    e1.printStackTrace();
                    return null;
                }
            } else {
                System.out.println("no++");
                return null;
            }

        } catch (Exception e) {
            System.out.println(e);
            return null;
        }

    }



    /**
     * 从网络Url中下载文件
     * @param urlStr
     * @param fileName
     * @param savePath
     */
    public static String downLoadFromUrl(String urlStr, String fileName, String savePath) {
        try {
            URL url = new URL(urlStr);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            // 设置超时间为3秒
            conn.setConnectTimeout(3 * 1000);
            // 防止屏蔽程序抓取而返回403错误
            conn.setRequestProperty("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt)");

            // 得到输入流
            InputStream inputStream = conn.getInputStream();
            // 获取自己数组
            byte[] getData = readInputStream(inputStream);

            // 文件保存位置
            File saveDir = new File(savePath);
            if (!saveDir.exists()) {
                saveDir.mkdir();
            }
            File file = new File(saveDir + File.separator + fileName);
            FileOutputStream fos = new FileOutputStream(file);
            fos.write(getData);
            if (fos != null) {
                fos.close();
            }
            if (inputStream != null) {
                inputStream.close();
            }
            // System.out.println("info:"+url+" download success");
            return saveDir + File.separator + fileName;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "";

    }

    /**
     * 从输入流中获取字节数组
     * @param inputStream
     * @return
     */
    public static byte[] readInputStream(InputStream inputStream) throws IOException {
        byte[] buffer = new byte[1024];
        int len = 0;
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        while ((len = inputStream.read(buffer)) != -1) {
            bos.write(buffer, 0, len);
        }
        bos.close();
        return bos.toByteArray();
    }
}
