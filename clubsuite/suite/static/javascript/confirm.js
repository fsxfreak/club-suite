$(document).ready(function() {
    $(".delete_member").submit(function() {
        return confirm("Are you sure to delete the member?")
    });
    $(".promote_member").submit(function(){
        return confirm("Are you sure to promote the member?");
    });
    $(".demote_member").submit(function(){
        return confirm("Are you sure to demote the member?");
    });

});
