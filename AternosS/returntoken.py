import js2py #type:ignore
import time

def convertToken (garbage):
    print("Finding Token")
    line1 = garbage.text.split('const COOKIE_PREFIX = "ATERNOS";')
    line2 = line1[1].split("</script>")
    line3 = line2[1].split("{window")
    time.sleep(5)

    func = '''
    //Decoder by broc.seib
    function atob(s) {
    var e={},i,b=0,c,x,l=0,a,r='',w=String.fromCharCode,L=s.length;
    var A="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for(i=0;i<64;i++){e[A.charAt(i)]=i;}
    for(x=0;x<L;x++){
        c=e[s.charAt(x)];b=(b<<6)+c;l+=6;
        while(l>=8){((a=(b>>>(l-=8))&0xff)||(x<(L-2)))&&(r+=w(a));}
    }
    return r;
};
    function headache() {
        var dict = {}
        dict ''' + line3[1][:-6] + '''
        console.log(dict["AJAX_TOKEN"])
        return dict["AJAX_TOKEN"]
    }
    
    '''
    evaluate = js2py.EvalJs({'python_sum':sum})
    evaluate.execute(func)
    return evaluate.headache()