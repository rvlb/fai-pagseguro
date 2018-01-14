function getCookie(name) {
    var re = new RegExp(name + "=([^;]+)");
    var value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

var pagseguroSession = getCookie('pagseguro_session');
PagSeguroDirectPayment.setSessionId(pagseguroSession);

function submitForm(selectedOption, creditCardToken) {
    var form = document.getElementById('cart-form');

    var operationType = document.createElement('input');
    operationType.setAttribute('type', 'hidden');
    operationType.setAttribute('name', selectedOption);
    form.appendChild(operationType);

    var senderHashInput = document.createElement('input');
    senderHashInput.setAttribute('type', 'hidden');
    senderHashInput.setAttribute('name', 'sender-hash');
    senderHashInput.setAttribute('value', PagSeguroDirectPayment.getSenderHash());
    form.appendChild(senderHashInput);

    if(selectedOption === 'credit-card') {
        var creditCardTokenInput = document.createElement('input');
        creditCardTokenInput.setAttribute('type', 'hidden');
        creditCardTokenInput.setAttribute('name', 'card-token');
        creditCardTokenInput.setAttribute('value', creditCardToken);
        form.appendChild(creditCardTokenInput);
    }
    form.submit();
}

document.getElementById('bank-slip-btn').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('credit-card-btn').setAttribute('disabled', true);
    this.setAttribute('disabled', true);
    submitForm('bank-slip');
});

document.getElementById('credit-card-btn').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('bank-slip-btn').setAttribute('disabled', true);
    this.setAttribute('disabled', true);
    PagSeguroDirectPayment.createCardToken({
        cardNumber: '4111111111111111',
        cvv: '123',
        expirationMonth: '12',
        expirationYear: '2030',
        success: function(response) {
            console.log(response);
            var creditCardToken = response.card.token;
            submitForm('credit-card', creditCardToken);
        },
        error: function(error) {
            console.log(error);
        }
    });
});