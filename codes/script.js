$(document).ready(function () {
  const $resultContainer = $('.result-container');
  const $gridBox = $('.grid-box');
  const apiUrlPrefix = 'http://127.0.0.1:5000'; // 设置请求前缀

  // 当文本框内容变化时
  $('#generate-similar').on('click', function (event) {
    event.preventDefault();

    // 清除之前的处理结果
    $('#classification-result').empty();
    $('#generated-image').attr(
      'src',
      'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    );
    // submit改成resubmit
    event.target.innerText = 'Resubmit';

    // 显示右侧内容
    $resultContainer.removeClass('hidden').addClass('show slide-in-right');
    $gridBox.removeClass('grid-cols-1').addClass('grid-cols-2');

    // 处理文本输入
    const text = $('#text-input').val();

    // 生成相似图像
    $.ajax({
      url: `${apiUrlPrefix}/generate`,
      method: 'POST',
      data: JSON.stringify({ text: text }),
      contentType: 'application/json',
      beforeSend: function () {
        $('.result .overlay').addClass('fade-in');
        $('.result .overlay').show('slow');
        $('.center').removeClass('fit-size');
      },
      complete: function () {
        $('.result .overlay').removeClass('fade-in');
        $('.result .overlay').hide();
        $('.center').addClass('fit-size');
      },
      success: function (data) {
        if (data.image) {
          $('#generated-image').attr('src', data.image);
        } else {
          console.error('Invalid image data');
        }
      },
      error: function (error) {
        console.error(error);
      },
    });
  });
});
