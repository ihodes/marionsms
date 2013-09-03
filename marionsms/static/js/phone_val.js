$.fn.phone_numberify = phone_numberify;


function phone_numberify(hidden_field_sel, prefix) {
    var $el = $(this);
    $el.keyup(function() {
        var validated = validate_phone_number($el.val());
        if (validated) {
            $el.parent().removeClass('has-error');
            var final_no = validated
            if(prefix)
                final_no = prefix + final_no;
            $(hidden_field_sel).val(final_no);
        } else {
            $el.parent().addClass('has-error');
            $(hidden_field_sel).val($el.val());
        }
    });
}


function validate_phone_number(phone_number) {
    var pn_re = /\+?1?\s*[-\\\/\.]?\s*\(?(\d{3})\)?\s*[-\.\/\\]?\s*(\d{3})\s*[-\.\/\\]?\s*(\d{4})\s*/;
    var validated = pn_re.exec(phone_number);
    if (validated) {
        var validated_number = validated[1] + validated[2] + validated[3];
        return validated_number;
    } else {
        return false;
    }    
}
