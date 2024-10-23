
document.addEventListener('DOMContentLoaded', function () {
    const homeLink = document.getElementById('home-link');
    const subcategories = document.getElementById('subcategories');
    // const pisosLink = document.getElementById('pisos-link');
    // const subcategoriasPisos = document.querySelector('.subcategorias_pisos');
    // const adLink = document.getElementById('ad-link');
    // const subcategoriasAd = document.querySelector('.subcategorias_ad');
    // const murosLink = document.getElementById('muros-link');
    // const subcategoriasMuros = document.querySelector('.subcategorias_muros');

    // Maneja el clic en "HOME"
    homeLink.addEventListener('click', function (event) {
        event.preventDefault();
        subcategories.style.display = subcategories.style.display === "block" ? "none" : "block";
    });

    // Maneja el clic en "PISOS"
    // pisosLink.addEventListener('click', function (event) {
    //     event.preventDefault();
    //     const isVisible = subcategoriasPisos.style.display === 'block';
    //     subcategoriasPisos.style.display = isVisible ? 'none' : 'block';
    //     subcategoriasAd.style.display = 'none'; // Cierra subcategorías de "Muros"
    //     subcategoriasMuros.style.display = 'none'; // Cierra subcategorías de "Adhesivos"
    // });

    // Maneja el clic en "MUROS"
    // murosLink.addEventListener('click', function (event) {
    //     event.preventDefault();
    //     const isVisible = subcategoriasMuros.style.display === 'block';
    //     subcategoriasMuros.style.display = isVisible ? 'none' : 'block';
    //     subcategoriasPisos.style.display = 'none'; // Cierra subcategorías de "Pisos"
    //     subcategoriasAd.style.display = 'none'; // Cierra subcategorías de "Adhesivos"
    // });

    // Maneja el clic en "ADHESIVOS"
    // adLink.addEventListener('click', function (event) {
    //     event.preventDefault();
    //     const isVisible = subcategoriasAd.style.display === 'block';
    //     subcategoriasAd.style.display = isVisible ? 'none' : 'block';
    //     subcategoriasPisos.style.display = 'none'; // Cierra subcategorías de "Pisos"
    //     subcategoriasMuros.style.display = 'none'; // Cierra subcategorías de "Muros"
    // });

    // Cierra subcategorías y el menú de categorías al hacer clic fuera
    document.addEventListener('click', function (event) {
        if (!homeLink.contains(event.target) && !subcategories.contains(event.target)) {
            subcategories.style.display = 'none'; // Oculta el menú de categorías
        }

        // if (!pisosLink.contains(event.target) && !subcategoriasPisos.contains(event.target)) {
        //     subcategoriasPisos.style.display = 'none'; // Oculta subcategorías de "Pisos"
        // }

        // if (!adLink.contains(event.target) && !subcategoriasAd.contains(event.target)) {
        //     subcategoriasAd.style.display = 'none'; // Oculta subcategorías de "Adhesivos"
        // }

        // if (!murosLink.contains(event.target) && !subcategoriasMuros.contains(event.target)) {
        //     subcategoriasMuros.style.display = 'none'; // Oculta subcategorías de "Muros"
        // }
    });
});

        
   


   
        function abrirModalRegistro() {
          var modal = new bootstrap.Modal(document.getElementById('modalRegistroProveedor'));
          modal.show();
        }
        document.getElementById('registroProveedor').addEventListener('click', function() {
          abrirModalRegistro();
        });

        $(document).ready(function(){
            $("#buscarproveedor").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                var noMatch = true;
                $("#tabla_proveedores tbody tr").filter(function() {
                    var match = $(this).text().toLowerCase().indexOf(value) > -1;
                    $(this).toggle(match);
                    if (match) noMatch = false;
                });
                if (noMatch) {
                    $("#noMatches").show();
                } else {
                    $("#noMatches").hide();
                }
            });
        });
        

        document.getElementById('foto').addEventListener('change', function(event) {
            const file = event.target.files[0];
            const preview = document.getElementById('preview');
        
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    preview.src = e.target.result; // Establece la fuente de la imagen a la cargada
                    preview.style.display = 'block'; // Muestra la imagen
                }
        
                reader.readAsDataURL(file); // Lee el archivo como una URL de datos
            } else {
                preview.src = ""; // Reinicia la fuente si no hay archivo
                preview.style.display = 'none'; // Oculta la imagen
            }
        });
        



        document.addEventListener('DOMContentLoaded', function() {
            var editarProveedorModal = document.getElementById('editarModalProveedor');
        
            editarProveedorModal.addEventListener('show.bs.modal', function(event) {
                var button = event.relatedTarget; // Botón que activó el modal
                var id = button.getAttribute('data-id');
                var nombre = button.getAttribute('data-nombre');
                var telefono = button.getAttribute('data-telefono');
                var correo = button.getAttribute('data-correo');
                var direccion = button.getAttribute('data-direccion');
                var foto = button.getAttribute('data-foto');
        
                // Asigna los valores a los campos del formulario
                editarProveedorModal.querySelector('#editarproveedorId').value = id;
                editarProveedorModal.querySelector('#nombreeditar').value = nombre;
                editarProveedorModal.querySelector('#telefonoeditar').value = telefono;
                editarProveedorModal.querySelector('#correoeditar').value = correo;
                editarProveedorModal.querySelector('#direccioneditar').value = direccion;
        
                // Carga la imagen
                const previeweditar = editarProveedorModal.querySelector('#previeweditar');
                if (foto) {
                    previeweditar.src = "/static/uploads/" + foto; // Asigna la URL de la imagen
                    previeweditar.style.display = 'block'; // Muestra la imagen
                } else {
                    previeweditar.src = ""; // Si no hay imagen, reinicia
                    previeweditar.style.display = 'none';
                }
            });
        
            // Manejador para la vista previa de la nueva imagen
            document.getElementById('fotoeditar').addEventListener('change', function(event) {
                const file = event.target.files[0];
                const previeweditar = document.getElementById('previeweditar');
        
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previeweditar.src = e.target.result; // Establece la fuente de la imagen a la cargada
                        previeweditar.style.display = 'block'; // Muestra la imagen
                    }
                    reader.readAsDataURL(file); // Lee el archivo como una URL de datos
                } else {
                    previeweditar.src = ""; // Reinicia la fuente si no hay archivo
                    previeweditar.style.display = 'none'; // Oculta la imagen
                }
            });
        });
        


        document.addEventListener('DOMContentLoaded', function() {
            var eliminarModal = document.getElementById('eliminarProveedor');
            eliminarModal.addEventListener('show.bs.modal', function (event) {
                var button = event.relatedTarget;
                var proveedorId = button.getAttribute('data-id');
                var formEliminar = document.getElementById('formEliminarPro');
                formEliminar.action = '/eliminar_proveedor/' + proveedorId;
            });
        });
        
        
            
            

           
                