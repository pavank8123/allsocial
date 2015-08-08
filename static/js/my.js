$(document).ready(function(){

	$( "#search" ).bind( "keydown", function( event ) {
        var m = event.keyCode
        if ( m === $.ui.keyCode.TAB &&
                $( this ).data( "autocomplete" ).menu.active ) {
            event.preventDefault();
        }
        if($("#day-select").val()==0){
            $("#footprint-error").text('Please select circulation type to select media.');
            return false;
        }else{
            $("#footprint-error").text('');
        }
    }).autocomplete({
        source: function( request, response ) {
            $.getJSON( '/getusernames/', {term: extractLast( request.term )}, response );
        },
        search: function() {
            // custom minLength
            var term = extractLast( this.value );
            if ( term.length < 1 ) {return false;}
        },
        focus: function() {
            // prevent value inserted on focus
            return false;
        },
        select: function( event, ui ) {
            var terms = split( this.value );            
            // remove the current input
            terms.pop();
            // add the selected item
            terms.push( ui.item.value );
            // add placeholder to get the comma-and-space at the end
            terms.push( "" );
            this.value = terms.join('');            
            
        }
    });
    function extractLast(term) {
        return split(term).pop();
    }
    function split(val) {
        //return val.split(/,\s*/);
        return val.split(",");
    }
})