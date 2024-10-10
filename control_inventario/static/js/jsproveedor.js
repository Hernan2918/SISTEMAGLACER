
document.addEventListener('DOMContentLoaded', function () {
    const homeLink = document.getElementById('home-link');
    const subcategories = document.getElementById('subcategories');
    const pisosLink = document.getElementById('pisos-link');
    const subcategoriasPisos = document.querySelector('.subcategorias_pisos');
    const adLink = document.getElementById('ad-link');
    const subcategoriasAd = document.querySelector('.subcategorias_ad');
    const murosLink = document.getElementById('muros-link');
    const subcategoriasMuros = document.querySelector('.subcategorias_muros');

    // Maneja el clic en "HOME"
    homeLink.addEventListener('click', function (event) {
        event.preventDefault();
        subcategories.style.display = subcategories.style.display === "block" ? "none" : "block";
    });

    // Maneja el clic en "PISOS"
    pisosLink.addEventListener('click', function (event) {
        event.preventDefault();
        const isVisible = subcategoriasPisos.style.display === 'block';
        subcategoriasPisos.style.display = isVisible ? 'none' : 'block';
        subcategoriasAd.style.display = 'none'; // Cierra subcategorías de "Muros"
        subcategoriasMuros.style.display = 'none'; // Cierra subcategorías de "Adhesivos"
    });

    // Maneja el clic en "MUROS"
    murosLink.addEventListener('click', function (event) {
        event.preventDefault();
        const isVisible = subcategoriasMuros.style.display === 'block';
        subcategoriasMuros.style.display = isVisible ? 'none' : 'block';
        subcategoriasPisos.style.display = 'none'; // Cierra subcategorías de "Pisos"
        subcategoriasAd.style.display = 'none'; // Cierra subcategorías de "Adhesivos"
    });

    // Maneja el clic en "ADHESIVOS"
    adLink.addEventListener('click', function (event) {
        event.preventDefault();
        const isVisible = subcategoriasAd.style.display === 'block';
        subcategoriasAd.style.display = isVisible ? 'none' : 'block';
        subcategoriasPisos.style.display = 'none'; // Cierra subcategorías de "Pisos"
        subcategoriasMuros.style.display = 'none'; // Cierra subcategorías de "Muros"
    });

    // Cierra subcategorías y el menú de categorías al hacer clic fuera
    document.addEventListener('click', function (event) {
        if (!homeLink.contains(event.target) && !subcategories.contains(event.target)) {
            subcategories.style.display = 'none'; // Oculta el menú de categorías
        }

        if (!pisosLink.contains(event.target) && !subcategoriasPisos.contains(event.target)) {
            subcategoriasPisos.style.display = 'none'; // Oculta subcategorías de "Pisos"
        }

        if (!adLink.contains(event.target) && !subcategoriasAd.contains(event.target)) {
            subcategoriasAd.style.display = 'none'; // Oculta subcategorías de "Adhesivos"
        }

        if (!murosLink.contains(event.target) && !subcategoriasMuros.contains(event.target)) {
            subcategoriasMuros.style.display = 'none'; // Oculta subcategorías de "Muros"
        }
    });
});

        
   


   
        function abrirModalRegistro() {
          var modal = new bootstrap.Modal(document.getElementById('modalRegistroProveedor'));
          modal.show();
        }
        document.getElementById('registroProveedor').addEventListener('click', function() {
          abrirModalRegistro();
        });
    


    
        document.addEventListener('DOMContentLoaded', function() {
            var editarProductoModal = document.getElementById('editarModalProducto');
            editarProductoModal.addEventListener('show.bs.modal', function(event) {
                var button = event.relatedTarget;
                var id = button.getAttribute('data-id');
                var medida = button.getAttribute('data-medidas');
                var proveedor = button.getAttribute('data-proveedor');
                var producto = button.getAttribute('data-producto');
                var calidad = button.getAttribute('data-calidad');
                var existencias = button.getAttribute('data-existencias');
                var rotas = button.getAttribute('data-rotas');
                var precio = button.getAttribute('data-precio');
                var embalaje = button.getAttribute('data-embalaje');
                var ubicacion = button.getAttribute('data-ubicacion');
                var categoria = button.getAttribute('data-categoria');
        
                var inputId = editarProductoModal.querySelector('#editarproductoId');
                var inputMedida = editarProductoModal.querySelector('#medidaeditar');
                var inputproveedor = editarProductoModal.querySelector('#proveedoreseditar');
                var inputproducto = editarProductoModal.querySelector('#productoeditar');
                var inputCalidad = editarProductoModal.querySelector('#calidadeditar');
                var inputExistencias = editarProductoModal.querySelector('#existenciaeditar');
                var inputRotas = editarProductoModal.querySelector('#rotaseditar');
                var inputPrecio = editarProductoModal.querySelector('#precioeditar');
                var inputEmbalaje = editarProductoModal.querySelector('#embalajeeditar');
                var inputUbicacion = editarProductoModal.querySelector('#ubicacioneditar');
                var inputCategoria = editarProductoModal.querySelector('#categoriaseditar');
        
                inputId.value = id;
                inputMedida.value = medida;
                inputproducto.value= producto;
                inputCalidad.value = calidad;
                inputExistencias.value = existencias;
                inputRotas.value = rotas;
                inputPrecio.value=precio;
                inputEmbalaje.value = embalaje;
                inputUbicacion.value = ubicacion;
                
            
        
                // Seleccionar la opción correcta en el select de docente
              Array.from(inputproveedor.options).forEach(option => {
                  if (option.value == proveedor) {
                      option.selected = true;
                  } else {
                      option.selected = false;
                  }
              });
      
              // Seleccionar la opción correcta en el select de escuela
              Array.from(inputCategoria.options).forEach(option => {
                  if (option.value == categoria) {
                      option.selected = true;
                  } else {
                      option.selected = false;
                  }
              });
            });
        });
        


        
            document.addEventListener('DOMContentLoaded', function() {
                var eliminarModal = document.getElementById('eliminarP');
                eliminarModal.addEventListener('show.bs.modal', function (event) {
                    var button = event.relatedTarget;
                    var productoId = button.getAttribute('data-id');
                    
                    
                      
                  
                    var formEliminar = document.getElementById('formEliminar');
                    formEliminar.action = '/eliminar_producto/' + productoId;
                });
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
                