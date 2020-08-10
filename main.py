from jumper import jumper
import atexit


if __name__ == '__main__':
    jumper.crawler("https://blog.naver.com/PostView.nhn?blogId=una5894&logNo=220837664682&parentCategoryNo=&categoryNo=84&viewDate=&isShowPopularPosts=false&from=postView#", "Stranger", 0,0,5)
    atexit.register(printexit)