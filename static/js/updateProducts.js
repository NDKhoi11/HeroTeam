// call ajax to update product after filter or search
function loadAjax(category_req, search_req) {
  const filter_Obj = {}

  // get request from URL
  const req = window.location.search.split('=')
  // hidden slide and category list if request exits
  $(".portfolio").css('display', req[0] ? 'none' : 'visible')
  $(".slide").css('display', req[0] ? 'none' : 'visible')

  filter_Obj["category_req"] = req[0].includes('category') ? decodeURIComponent(req[1]) : 'None'
  filter_Obj["search_req"] = req[0].includes('search') ? decodeURIComponent(req[1]) : 'None'
  filter_Obj["order-by"] = $("#order-by").children("option:selected").val()
  filter_Obj["promotion"] = $("#promotion").children("option:selected").val()
  filter_Obj["available"] = $("#available").children("option:selected").val()

  $.ajax({
    url: '/filter-data',
    data: filter_Obj,
    dataType: 'json',
    success: function (res) {
      $(".product-list").html(res.data)
    }
  }
  )
}