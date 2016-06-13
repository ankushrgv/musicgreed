$(document).on('ready', function(){

	$('.active').removeClass('cls_tab');

	$(document).on('click','.string-name', function(event){
        $this = $(this);

        $(document).find('.active').addClass('cls_tab');
        $(document).find('.active').removeClass('active');

        $this.addClass('active');    
    });

    $(document).on('click','.search-box input#search_text', function(event){
        $this = $(this);
        $this.val('');
    });

    $(document).on('click','.search-box input#track_tab_search_text', function(event){
        $this = $(this);
        $this.val('');
    });

    $(document).on('click', '.add-new', function(event){
        event.preventDefault();

        var modal = document.getElementById('myModal');
        var span = document.getElementsByClassName("close")[0];
        
        modal.style.display = "block";

        span.onclick = function() {
            modal.style.display = "none";
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        $('.add-new-form').validate({
            rules:{
                'track':{
                    required:true,
                    minlength:1,
                    maxlength:150
                },
                'artist':{
                    required:true,
                    minlength:2,
                    maxlength:80
                },
                'genre':{
                    required:true,
                    minlength:2,
                    maxlength:30
                },
                'album':{
                    required:true,
                    minlength:1,
                    maxlength:50
                },
                'rating':{
                    required:true
                },
            },
            messages:{
                'track':{
                    required:'Track is required',
                    minlength:'Track should have atleast 1 characters',
                    maxlength:'Track should have less than 150 characters'
                },
                'artist':{
                    required:'Artist is required',
                    minlength:'Artist should have atleast 2 characters',
                    maxlength:'Artist should have less than 80 characters'
                },
                'genre':{
                    required:'Genre is required',
                    minlength:'Genre should have atleast 2 characters',
                    maxlength:'Genre should have less than 30 characters'
                },
                'album':{
                    required:'Album is required',
                    minlength:'Album should have atleast 1 characters',
                    maxlength:'Album should have less than 50 characters'
                },
                'rating':{
                    required:'Rating is required',
                },
            },
            ignore:[],
            onfocusout:function(element) {
                $(element).valid();
            },
            highlight:function(el) {
                $(el).addClass('redborder');
            },

            unhighlight:function(el){
                $(el).removeClass('redborder');
            },
            invalidHandler: function(event, validator) {
                console.log(event);
            },
            submitHandler: function(form){
                addnew_form_submit(t_url, t_form, t_msg);
            }
        });

        var t_url = "/addnew_form_submit/";
        var t_form = "#add-new-form";
        var t_msg = "Added Succesfully";

        $(document).on('click','.add-new-form-container button#submit-form', function(event){        
            event.preventDefault();

            $this = $(this);
            var tab_type = $this.data("tab-type");

            if(tab_type == "track"){
                var t_msg = "New Track Data Submitted Succesfully!!";
                addnew_form_submit(t_url, t_form, t_msg);
            }

            else if(tab_type == "artist"){
                var t_msg = "New Artist Data Submitted Succesfully!!";
                addnew_form_submit(t_url, t_form, t_msg);
            }

            else if(tab_type == "genre"){
                var t_msg = "New Genre Data Submitted Succesfully!!";
                addnew_form_submit(t_url, t_form, t_msg);
            }

            else if(tab_type == "album"){
                var t_msg = "New Album Data Submitted Succesfully!!";
                addnew_form_submit(t_url, t_form, t_msg);
            }
        });
    });

    $('.edit-submit').hide();
    $(document).on('click','.edit-button', function(event){
    	$('.edit-submit').show();
    	$('.edit-button').hide();
    	$('#id_title').removeAttr("disabled").attr("id", "editable");
    	$('#id_artist').removeAttr("disabled").attr("id", "editable");
    	$('#id_album').removeAttr("disabled").attr("id", "editable");
    	$('#id_genre').removeAttr("disabled").attr("id", "editable");
    	$('#id_rating').removeAttr("disabled").attr("id", "editable");
    });
});


function addnew_form_submit(f_url, form, msg) {

    $.ajax({
           type: "POST",
           url: f_url,
           data: $(form).serialize(),
           // dataType: 'json',

           success: function(data){
                if(alert(msg)){}
                else
                    window.location.reload(); 
           }
    });
}