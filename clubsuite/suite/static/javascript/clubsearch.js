/*
$(document).ready(function() {
    console.log("JavaScript Connected")
    initializePage();
});

function initializePage() {
	$('.box').click(addClubDetails);

}

function addClubDetails(e) {
	// Prevent following the link
	e.preventDefault();

	var clubId = $(this).closest('.box').attr('id');

  //var idNumber = clubId.substr('box'.length);

	//$.get("/club/" + idNumber, addImage.bind(this));
  console.log(clubId);
  //var projectDetails = '<p>hello</p>';
  $(this).append(projectDetails);
	$(this).siblings('.details').html(projectDetails);
}


function addImage(result) {
	console.log(result);
	var idNumber = result.id;
	var projectDetails = '<p>hello</p><img src="' + result['image'] + '" class="img">';
	console.log($('.details'));
	$(this).siblings('.details').html(projectDetails);


}
*/
