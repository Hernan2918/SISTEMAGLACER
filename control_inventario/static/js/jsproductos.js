
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
          var modal = new bootstrap.Modal(document.getElementById('modalRegistro'));
          modal.show();
        }
        document.getElementById('registroProducto').addEventListener('click', function() {
          abrirModalRegistro();
        });
    
        

        document.addEventListener('DOMContentLoaded', function() {
            var editarProductoModal = document.getElementById('editarModalProducto');
            editarProductoModal.addEventListener('show.bs.modal', function(event) {
                var button = event.relatedTarget;
                var id = button.getAttribute('data-id');
                var medidas = button.getAttribute('data-medidas');
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
                var inputProveedor = editarProductoModal.querySelector('#proveedoreditar');
                var inputProducto = editarProductoModal.querySelector('#productoeditar');
                var inputCalidad = editarProductoModal.querySelector('#calidadeditar');
                var inputExistencias = editarProductoModal.querySelector('#existenciaeditar');
                var inputRotas = editarProductoModal.querySelector('#rotaseditar');
                var inputPrecio = editarProductoModal.querySelector('#precioeditar');
                var inputEmbalaje = editarProductoModal.querySelector('#embalajeeditar');
                var inputUbicacion = editarProductoModal.querySelector('#ubicacioneditar');
                var inputCategoria = editarProductoModal.querySelector('#categoriaeditar');
        
                inputId.value = id;
                inputMedida.value = medidas;
                inputProducto.value = producto;
                inputCalidad.value = calidad;
                inputExistencias.value = existencias;
                inputRotas.value = rotas;
                inputPrecio.value = precio;
                inputEmbalaje.value = embalaje;
                inputUbicacion.value = ubicacion;
                
      
                Array.from(inputProveedor.options).forEach(option => {
                    option.selected = option.value === proveedor;
                });
        
                // Seleccionar la categoría registrada
                Array.from(inputCategoria.options).forEach(option => {
                    option.selected = option.value === categoria;
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
                

                
                document.getElementById('Descargar').addEventListener('click', async function() {
                    const { jsPDF } = window.jspdf;
                    const doc = new jsPDF();
                    async function getBase64ImageFromUrl(url) {
                        const res = await fetch(url);
                        const blob = await res.blob();
                        return new Promise((resolve, reject) => {
                            const reader = new FileReader();
                            reader.onloadend = () => resolve(reader.result);
                            reader.onerror = reject;
                            reader.readAsDataURL(blob);
                        });
                    }
                    const imgUrl1 = 'static/img/logov.jpeg';
                    
                    const imgData1 = await getBase64ImageFromUrl(imgUrl1);
                    
              
                    doc.addImage(imgData1, 'PNG', 10, 5, 20, 20);
                    
              
                    const table = document.getElementById("tabla_productos");
                    const rows = [];
              
                    for (let i = 1; i < table.rows.length; i++) {
                        const row = table.rows[i];
                        const rowData = [];
                        for (let j = 0; j < row.cells.length - 1; j++) {
                            rowData.push(row.cells[j].innerText);
                        }
                        rows.push(rowData);
                    }
                    doc.setFontSize(13);
                    doc.text('PRODUCTOS', 105, 20, { align: 'center' });
                    doc.text('GLACER Glamur Cerámico', 200, 15, { align: 'right' });
                    doc.setTextColor(255, 0, 0);
                    doc.text('Atlacomulco Vías', 200, 20, { align: 'right' } );
                    
                    doc.autoTable({
                        head: [['Medida', 'Proveedor', 'Nombre', 'Calidad', 'Existencia', 'Rotas', 'Precio', 'Embalaje', 'Ubicacion', 'Categoria']],
                        body: rows,
                        theme: 'grid',
                        styles: { halign: 'center' },
                        headStyles: { fillColor: [255, 0, 0] }, // Color verde
                        startY: 30 
                    });
              
                    doc.save('tabla_pisos.pdf');
                });