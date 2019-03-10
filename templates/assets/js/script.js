//big explore function

function open_explore(){
    if (document.getElementById("isi-explore-big").style.display === "block") { 
        document.getElementById("isi-explore-big").style.display = "none";
    }
    else{
        document.getElementById("isi-explore-big").style.display = "block";
    }
}

//small explore function

function open_kategori(){
    if (document.getElementById("isi-kategori").style.display === "block") { 
        document.getElementById("isi-kategori").style.display = "none";
    }
    else{
        document.getElementById("isi-kategori").style.display = "block";
    }
}

function open_penulis(){
    if (document.getElementById("isi-penulis").style.display === "block") { 
        document.getElementById("isi-penulis").style.display = "none";
    }
    else{
        document.getElementById("isi-penulis").style.display = "block";
    }
}

function open_penerbit(){
    if (document.getElementById("isi-penerbit").style.display === "block") { 
        document.getElementById("isi-penerbit").style.display = "none";
    }
    else{
        document.getElementById("isi-penerbit").style.display = "block";
    }
}

//login

function login(){
    document.getElementById("login").style.display = "block";
}

function close_login(){
    document.getElementById("login").style.display = "none";
}

//small footer function

function open_bukuku(){
    if (document.getElementById("isi-bukuku").style.display === "block") { 
        document.getElementById("isi-bukuku").style.display = "none";
    }
    else{
        document.getElementById("isi-bukuku").style.display = "block";
    }
}

function open_beli(){
    if (document.getElementById("isi-beli").style.display === "block") { 
        document.getElementById("isi-beli").style.display = "none";
    }
    else{
        document.getElementById("isi-beli").style.display = "block";
    }
}

function open_jual(){
    if (document.getElementById("isi-jual").style.display === "block") { 
        document.getElementById("isi-jual").style.display = "none";
    }
    else{
        document.getElementById("isi-jual").style.display = "block";
    }
}

function open_bantuan(){
    if (document.getElementById("isi-bantuan").style.display === "block") { 
        document.getElementById("isi-bantuan").style.display = "none";
    }
    else{
        document.getElementById("isi-bantuan").style.display = "block";
    }
}

function minusFunction(){
    qtyNow = document.getElementById("book-qty").value;
    if (parseInt(qtyNow) > 1){
        qtyNew = parseInt(qtyNow) - 1;
        document.getElementById("book-qty").value = qtyNew;
    }
}

function plusFunction(){
    qtyNow = document.getElementById("book-qty").value;
    qtyNew = parseInt(qtyNow) + 1;
    document.getElementById("book-qty").value = qtyNew;
}