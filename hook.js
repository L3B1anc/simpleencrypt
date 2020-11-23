
// hook some method
Java.perform(function () {
    console.log("[*] Hooking ...");
    // var clazz = Java.use("java.lang.Class");
    // var hclass = Java.use("okhttp3.HttpUrl");

    var clazz = Java.use("java.lang.Class");
    var hclass = Java.use("com.*.CryptoUtil");
    // hook encryptdata
    hclass.encryptDataWithSM.implementation = function (a,b,c) {
        send(arguments[1])
        var op = recv(function(value) {
            console.log("[*] js recv encryptdata content: " + value);
            b =  value;
        });
        op.wait();
        return this.encryptDataWithSM(a,b,c);
    };

    // hook decryptdata
    hclass.decryptDataWithSM.implementation = function(a,b,c){
        var getVal = this.decryptDataWithSM(a,b,c)
        send(getVal)
        var op = recv(function(value){
            console.log("[*] js recv decryptdata content: "+value);
            getVal = value;
        });
        op .wait();
        return getVal;

    };
});