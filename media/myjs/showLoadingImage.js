showLoadingImage = {
    //Show "Loading image"
    show_loading: function(){
        //Shows moving loading gif after form submit
        $("#loading").show("fast");
        //this.preventDefault();
        var form = $(this).unbind('submit');
        setTimeout(function(){
            form.submit();
            $("#loading").hide();
        }, 9000);
    }
}
