function initMap(latitude, longitude, is_call=false) {
    if(is_call == true){
        $('#emplacement').css( "display", "block" );
        var zoom = 13
        var position = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
    }
    else {
        var zoom = 1
        var uluru = {lat: parseFloat(0), lng: parseFloat(0)};
    }

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: zoom,
      center: position
    });
    var marker = new google.maps.Marker({
      position: position,
      map: map
    });
}

$(function() {
    $('#button').click(function() {
        $('#contain_loader').css( "display", "block" );
        $('#content_description').css( "display", "none" );
        $('#emplacement').css( "display", "none" );
        $('#alert').css( "display", "none" );
        var request = $('form').serialize();
        $.ajax({
            url: '/get_user_request',
            data: request,
            type: 'GET',
            success: function(response) {
                $('#contain_loader').css( "display", "none" );
                var response_json = JSON.parse(response)
                console.log(response_json)
                if (response_json['type_search'] == 'place'){
                    if (response_json['error_place'] == false){
                        adresse = response_json['emplacement']['adresse']
                        $('#emplacement').css( "display", "block" ).css("margin-top", "3%");
                        $('#adresse').text(response_json['sentance_place'] + adresse);
                        latitude = response_json['emplacement']['latitude']
                        longitude = response_json['emplacement']['longitude']
                        initMap(latitude, longitude, true)
                    } else {
                        $('#alert').css( "display", "block" );
                        $('#text_error').text("Ton emplacement est introuvable ! ou alors c'est ma memoire qui me fait defaut :)");
                    }

                }
                else if(response_json['type_search'] == 'description'){
                    if (response_json['error_description'] == false){
                        $('#description').text(response_json['sentance_description'] + response_json['description']);
                        $('#content_description').css( "display", "block").css("margin-top", "5%");
                    } else {
                        $('#alert').css( "display", "block" );
                        $('#text_error').text("Je ne connais pas d'histoire sur ce que tu me demande mon poussin :)");
                    }
                }
                else if(response_json['type_search'] == 'place description'){
                    if (response_json['error_description'] == true && response_json['error_place'] == true){
                        $('#alert').css( "display", "block" );
                        $('#text_error').text("Je ne connais ni l'histoire ni l'emplacement de ce que tu me demandes mon poussin :)");
                    } else {
                        if (response_json['error_description'] == false ){
                            $('#description').text(response_json['sentance_description'] + response_json['description']);
                            $('#content_description').css( "display", "block" ).css( "width", "950px" );
                        } else {
                            $('#alert').css( "display", "block" );
                            $('#text_error').text("Je ne connais pas d'histoire sur ce que tu me demande mon poussin :)");
                        }

                        if (response_json['error_place'] == false){
                            adresse = response_json['emplacement']['adresse']
                            $('#emplacement').css( "display", "block" ).css( "width", "920px" );

                            $('#adresse').text(response_json['sentance_place'] + adresse);

                            latitude = response_json['emplacement']['latitude']
                            longitude = response_json['emplacement']['longitude']
                            initMap(latitude, longitude, true)
                        } else{
                            $('#alert').css( "display", "block" );
                            $('#text_error').text("Ton emplacement est introuvable ! ou alors c'est ma memoire qui me fait defaut :)");
                        }
                    }
                }
                else {
                    console.log("erreur")
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});