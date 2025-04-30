package cn.edu.siso.test.test.beans;

public class News {
    String content,title;

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public News(String content, String title) {
        this.content = content;
        this.title = title;
    }
}
