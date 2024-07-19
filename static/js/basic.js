// 共通処理
// サイドバー

jQuery(function($){

    $(document).on('click', '.sidebar-menu-list li:nth-of-type(3)', function (e) {

        $(this).toggleClass("clicked");
        $(".sidebar-menu-list ul").slideToggle();

    });
});