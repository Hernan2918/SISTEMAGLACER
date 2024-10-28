
document.addEventListener('DOMContentLoaded', function () {
    const homeLink = document.getElementById('home-link');
    const subcategories = document.getElementById('subcategories');
    // const pisosLink = document.getElementById('pisos-link');
    // const subcategoriasPisos = document.querySelector('.subcategorias_pisos');
    // const adLink = document.getElementById('ad-link');
    // const subcategoriasAd = document.querySelector('.subcategorias_ad');
    // const murosLink = document.getElementById('muros-link');
    // const subcategoriasMuros = document.querySelector('.subcategorias_muros');

    homeLink.addEventListener('click', function (event) {
        event.preventDefault();
        subcategories.style.display = subcategories.style.display === "block" ? "none" : "block";
    });

    // pisosLink.addEventListener('click', function (event) {
    //     event.preventDefault();
    //     const isVisible = subcategoriasPisos.style.display === 'block';
    //     subcategoriasPisos.style.display = isVisible ? 'none' : 'block';
    //     subcategoriasAd.style.display = 'none'; 
    //     subcategoriasMuros.style.display = 'none'; 
    // });

    // murosLink.addEventListener('click', function (event) {
    //     event.preventDefault();
    //     const isVisible = subcategoriasMuros.style.display === 'block';
    //     subcategoriasMuros.style.display = isVisible ? 'none' : 'block';
    //     subcategoriasPisos.style.display = 'none'; 
    //     subcategoriasAd.style.display = 'none'; 
    // });

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
          var modal = new bootstrap.Modal(document.getElementById('modalRegistroTinacos'));
          modal.show();
        }
        document.getElementById('registroProducto').addEventListener('click', function() {
          abrirModalRegistro();
        });
    


    
        document.addEventListener('DOMContentLoaded', function() {
            var editarProductoModal = document.getElementById('editarModalProductoTinacos');
            editarProductoModal.addEventListener('show.bs.modal', function(event) {
                var button = event.relatedTarget;

                console.log("Botón:", button);
        console.log("Atributos:", {
            id: button.getAttribute('data-id'),
            proveedor: button.getAttribute('data-proveedor'),
            producto: button.getAttribute('data-producto'),
            litros: button.getAttribute('data-litros'),
            color: button.getAttribute('data-color'),
            existencias: button.getAttribute('data-existencias'),
            rotas: button.getAttribute('data-rotas'),
            precio: button.getAttribute('data-precio'),
            ubicacion: button.getAttribute('data-ubicacion'),
            categoria: button.getAttribute('data-categoria')
        });

                var id = button.getAttribute('data-id');
                var proveedor = button.getAttribute('data-proveedor') || '';
                var producto = button.getAttribute('data-producto');
                var litros = button.getAttribute('data-litros');
                var color = button.getAttribute('data-color');
                var existencias = button.getAttribute('data-existencias');
                var rotas = button.getAttribute('data-rotas');
                var precio = button.getAttribute('data-precio');
                var ubicacion = button.getAttribute('data-ubicacion');
                var categoria = button.getAttribute('data-categoria') || '';

                console.log("ID:", id);
                console.log("Proveedor:", proveedor);
                console.log("Categoría:", categoria);
        
                var inputId = editarProductoModal.querySelector('#editarproductoId');
                var inputproveedor = editarProductoModal.querySelector('#proveedoreseditar');
                var inputproducto = editarProductoModal.querySelector('#productoeditar');
                var inputLitros = editarProductoModal.querySelector('#litroseditar');
                var inputColor = editarProductoModal.querySelector('#coloreditar');
                var inputExistencias = editarProductoModal.querySelector('#existenciaeditar');
                var inputRotas = editarProductoModal.querySelector('#rotaseditar');
                var inputPrecio = editarProductoModal.querySelector('#precioeditar');
                var inputUbicacion = editarProductoModal.querySelector('#ubicacioneditar');
                var inputCategoria = editarProductoModal.querySelector('#categoriaseditar');
        
                inputId.value = id;
                inputproducto.value= producto;
                inputLitros.value= litros;
                inputColor.value= color;
                inputRotas.value = rotas;
                inputExistencias.value = existencias;
                inputPrecio.value=precio;
                inputUbicacion.value = ubicacion;
                
            
        
                Array.from(inputproveedor.options).forEach(option => {
                    option.selected = (option.value == proveedor);
                });
                
                Array.from(inputCategoria.options).forEach(option => {
                    option.selected = (option.value == categoria);
                });

                
        
            });
        });

        

        
            document.addEventListener('DOMContentLoaded', function() {
                var eliminarModal = document.getElementById('eliminarTinacos');
                eliminarModal.addEventListener('show.bs.modal', function (event) {
                    var button = event.relatedTarget;
                    var productoId = button.getAttribute('data-id');
                    var formEliminar = document.getElementById('formEliminar');
                    formEliminar.action = '/eliminar_tinacos/' + productoId;
                });
            });
            

           
                $(document).ready(function(){
                    $("#buscarproducto").on("keyup", function() {
                        var value = $(this).val().toLowerCase();
                        var noMatch = true;
                        $("#tabla_productos tbody tr").filter(function() {
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
                