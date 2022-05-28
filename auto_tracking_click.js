//pour bloquer les redirections de clics dans une page
// alert("debut de code")

var elems = document.querySelectorAll('a,button')
function stopDefAction(evt) {
	evt.preventDefault();
}

for (var i = 0, length = elems.length; i < length; i++) {
	var elem = elems[i];
	elem.addEventListener(
		'click', stopDefAction, false
		);
}

/* 
TODO :
remplacer les virgules par des points dans les track_zone et track_nom
Accès au mail depuis le header orange > Apparition du mail dans track_nom 
gestion HP aide et contact
tester sur Angular (Espace client)
gestion des modales
Gestion clic caroussel 

Sosh : 
tester sur env Sosh
*/

var anchors = document.querySelectorAll('a,button');
for (var i = 0, length = anchors.length; i < length; i++) {
	var anchor = anchors[i];
	anchor.addEventListener('click', function() {
		
		//get track_nom
		var track_nom = this.innerText == "" ? this.parentNode.querySelectorAll(".o-link-text")[0].innerText.toLowerCase() : this.innerText.toLowerCase()

		//get track_zone
		var zone = this;


		while (zone.parentElement.querySelector("h2, h1, h3, h4, nav, header, footer, #o-ribbon-right, #o-ribbon") == null && zone.tagName!="BODY"){
			zone = zone.parentElement;
		}
		
		if(zone.tagName!="BODY"){
			if(zone.tagName == "HEADER" || zone.tagName == "NAV" || (zone.getAttribute("id")=="o-ribbon") || (zone.getAttribute("id")=="o-ribbon-right")){
				var track_zone="mega_menu";
			}
			else if(zone.tagName=="FOOTER"){
				var track_zone="footer";
			}
			else{	
				while (zone.parentElement.querySelector("h2, h1") == null && zone.tagName!="BODY"){
					zone = zone.parentElement;
				}
				track_zone=zone.parentElement.querySelector("h2, h1").innerText.toLowerCase();
			}	
			//get track_cible
			if(typeof this.getAttribute("href") == null ? this.form.action : this.getAttribute("href") == null){
				var track_cible = "none";
			}else{
				var track_cible = this.getAttribute("href") == null ? this.form.action : this.getAttribute("href");
			}

			//format value
			track_nom = track_nom.normalize("NFD").replace(/[\u0300-\u036f]|\/|€|\?/g, "").replace(/\s/g, "_");
			track_zone = track_zone.normalize("NFD").replace(/[\u0300-\u036f]|\/|€|\?/g, "").replace(/\s/g, "_");
			jSoned=`{"type_element" : "${this.nodeName}" ,"url_site" : "${document.domain}", "track_nom": "${track_nom}", "track_zone": "${track_zone}", "track_cible": "${track_cible}"}`
			console.warn(JSON.stringify(jSoned));
		}
		else{
			if(typeof this.getAttribute("href") == null ? this.form.action : this.getAttribute("href") == null){
				var track_cible = "none";
			}else{
				var track_cible = this.getAttribute("href") == null ? this.form.action : this.getAttribute("href")
			}

			jSoned=`{"type_element": "${this.nodeName}","url_site": "${document.domain}", "track_nom": "${track_nom}", "track_zone": "${track_zone}", "track_cible": "${track_cible}"}`
			console.warn(JSON.stringify(jSoned));
		}

		//utag.link({"track_nom":track_nom,"track_zone":track_zone,"track_cible":track_cible,"auto_click":true})
	}, true);
};

document.addEventListener("DOMContentLoaded", function(){
	document.querySelector('#didomi-host').remove();
})


// alert("debut de code")