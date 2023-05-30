//测试该文件是否被正确加载
//alert("register.js")
function bindEmailCaptchaClick() {
 $("#captcha-btn").click(function (event){
  // $this: 代表的是当前按钮的jquery对象
    var $this = $(this);
  //阻止默认的事件
    event.preventDefault();
    var email = $("input[name='email']").val();
    $.ajax({
    // http://127.0.0.1:5000（默认有）
    //auth/captcha/email?email=xxx@qq.com
      url:"/captcha/email?email="+email,
      method:"GET",
      success:function(result){
        var code = result['code'];
        if(code == 200){
          var countdown = 10;
          // 开始倒计时之前，就取消按钮的点击事件
          $this.off("click");
          var timer = setInterval(function(){
            $this.text(countdown);
            countdown-=1;
            // 倒计时结束的时候执行
            if(countdown<=0){
              //清除定时器
              clearInterval(timer);
              // 将按钮的文字重新修改回来
              $this.text("获取验证码");
              // 重新绑定点击事件
              bindEmailCaptchaClick();
            }
          },1000);
//          alert("邮箱验证码发送成功！");
         }else{
          alert(result['message']);
         }
// 可在控制台打印查看是否正确      console.log(result);
      },
      fail:function(error){
        console.log(error);
      }
    })
  });
  }
 //整个网页都加载完毕之后在执行
$(function (){
  bindEmailCaptchaClick();
});

