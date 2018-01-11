function getCookie(name) {
    var re = new RegExp(name + "=([^;]+)");
    var value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

var pagseguroSession = getCookie('pagseguro_session');
PagSeguroDirectPayment.setSessionId(pagseguroSession);

var creditCardToken = undefined;
PagSeguroDirectPayment.createCardToken({
    cardNumber: '4111111111111111',
    cvv: '123',
    expirationMonth: '12',
    expirationYear: '2030',
    success: function(response) {
        console.log(response);
        creditCardToken = response.card.token;
    },
    error: function(error) {
        console.log(error);
    }
});

var selectedOption = undefined;
document.getElementById('credit-card-btn').addEventListener('click', function(e) {
    selectedOption = 'credit-card';
});

document.getElementById('cart-form').addEventListener('submit', function(e) {
    var senderHashInput = document.createElement('input');
    senderHashInput.setAttribute('type', 'hidden');
    senderHashInput.setAttribute('name', 'sender-hash');
    senderHashInput.setAttribute('value', PagSeguroDirectPayment.getSenderHash());
    this.appendChild(senderHashInput);

    if(selectedOption === 'credit-card') {
        var creditCardTokenInput = document.createElement('input');
        creditCardTokenInput.setAttribute('type', 'hidden');
        creditCardTokenInput.setAttribute('name', 'card-token');
        creditCardTokenInput.setAttribute('value', creditCardToken);
        this.appendChild(creditCardTokenInput);
    }
});