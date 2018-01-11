var senderHash;

window.onload(function() {
    var pagseguroSession = '';
    PagSeguroDirectPayment.setSessionId(pagseguroSession); 
    senderHash = PagSeguroDirectPayment.getSenderHash();
});