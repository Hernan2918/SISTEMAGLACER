
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
                var proveedor = button.getAttribute('data-proveedor');
                var producto = button.getAttribute('data-producto');
                var litros = button.getAttribute('data-litros');
                var color = button.getAttribute('data-color');
                var existencias = button.getAttribute('data-existencias');
                var rotas = button.getAttribute('data-rotas');
                var precio = button.getAttribute('data-precio');
                var ubicacion = button.getAttribute('data-ubicacion');
                var categoria = button.getAttribute('data-categoria');

                console.log("ID:", id);
                console.log("Proveedor:", proveedor);
                console.log("Categoría:", categoria);
        
                var inputId = editarProductoModal.querySelector('#editarproductoId');
                
                var inputproducto = editarProductoModal.querySelector('#productoeditar');
                var inputLitros = editarProductoModal.querySelector('#litroseditar');
                var inputColor = editarProductoModal.querySelector('#coloreditar');
                var inputExistencias = editarProductoModal.querySelector('#existenciaeditar');
                var inputRotas = editarProductoModal.querySelector('#rotaseditar');
                var inputPrecio = editarProductoModal.querySelector('#precioeditar');
                var inputUbicacion = editarProductoModal.querySelector('#ubicacioneditar');
                
        
                inputId.value = id;
                inputproducto.value= producto;
                inputLitros.value= litros;
                inputColor.value= color;
                inputRotas.value = rotas;
                inputExistencias.value = existencias;
                inputPrecio.value=precio;
                inputUbicacion.value = ubicacion;
                
            
        
                var inputproveedor = editarProductoModal.querySelector('#proveedoreseditar');
                Array.from(inputproveedor.options).forEach(option => {
                    option.selected = (option.value == proveedor); // Asegúrate de que `proveedor` tiene el valor correcto
                });
                
                var inputCategoria = editarProductoModal.querySelector('#categoriaseditar');
                Array.from(inputCategoria.options).forEach(option => {
                    option.selected = (option.value == categoria); // Asegúrate de que `categoria` tiene el valor correcto
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
                    // Obtén el valor del input sin eliminar los espacios al inicio y al final
                    var value = $(this).val();
                    var noMatch = true;
            
                    // Si el input está vacío, muestra todas las filas y oculta el mensaje de "sin coincidencias"
                    if (value === "") {
                        $("#tabla_productos tbody tr").show();
                        $("#noMatches").hide();
                        return;
                    }
            
                    // Si el input contiene solo espacios, oculta todas las filas y muestra el mensaje "sin coincidencias"
                    if (value.trim() === "") {
                        $("#tabla_productos tbody tr").hide();
                        $("#noMatches").show();
                        return;
                    }
            
                    // Filtra las filas en función del texto ingresado
                    $("#tabla_productos tbody tr").filter(function() {
                        var match = $(this).text().toLowerCase().indexOf(value.trim().toLowerCase()) > -1;
                        $(this).toggle(match);
                        if (match) noMatch = false;
                    });
            
                    // Muestra el mensaje si no hubo coincidencias; oculta si las hubo
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
                
                    // Agregar el logo
                    const imgUrl1 = '/static/img/logov.jpeg';
                
                    async function getBase64ImageFromUrl(url) {
                        try {
                            const res = await fetch(url);
                            if (!res.ok) {
                                console.error('Error en la respuesta:', res.status, res.statusText);
                                throw new Error('Error al cargar la imagen');
                            }
                            const blob = await res.blob();
                            const reader = new FileReader();
                
                            return new Promise((resolve, reject) => {
                                reader.onloadend = () => resolve(reader.result); // Resuelve con el resultado Base64
                                reader.onerror = reject; // Rechaza si hay un error
                                reader.readAsDataURL(blob);
                            });
                        } catch (error) {
                            console.error('Error al cargar la imagen:', error);
                            return null;
                        }
                    }
                
                    const imgData1 = await getBase64ImageFromUrl(imgUrl1);
                
                    if (imgData1) {
                        doc.addImage(imgData1, 'JPEG', 13, 6, 20, 20); // Añadir imagen al PDF
                
                        // Obtener los productos y agregarlos al PDF
                        const response = await fetch('/obtener_todos_tinacos');
                        const productos = await response.json();
                
                        const rows = productos.map(producto => [
                            producto.proveedor_nombre,
                            producto.nombre,
                            producto.litros,
                            producto.color,
                            producto.existencias,
                            producto.rotas,
                            producto.precio,
                            producto.ubicacion,
                            producto.categoria_nombre
                        ]);
                
                        doc.setFontSize(13);
                        doc.text('PRODUCTOS', 105, 15, { align: 'center' });
                        doc.setFontSize(10);
                        doc.text('DEPARTAMENTO: TINACOS', 105, 23, { align: 'center' });
                        doc.setFontSize(13);
                        doc.text('GLACER Glamur Cerámico', 195, 15, { align: 'right' });
                        doc.setTextColor(220, 0, 0);
                        doc.text('Atlacomulco Vías', 195, 23, { align: 'right' });
                
                        doc.autoTable({
                            head: [['Proveedor', 'Nombre', 'Litros', 'Color', 'Existencia', 'Rotas', 'Precio', 'Ubicacion', 'Categoria']],
                            body: rows,
                            theme: 'grid',
                            styles: { halign: 'center' },
                            headStyles: { fillColor: [220, 0, 0] }, // Color verde
                            startY: 30 
                        });
                
                        // Guardar el archivo PDF
                        doc.save('tabla_tinacos.pdf');
                    } else {
                        console.error("No se pudo cargar la imagen correctamente.");
                    }
                });
                

                document.getElementById("buscar").addEventListener("click", function() {
                    document.getElementById("buscarproducto").focus();
                });


                // FUNCION PARA VALIDAR EL REGISTRO DE UN PRODUCTO

                function validarFormularioproducto() {
                    var isValid = true;
                
                    var producto = document.getElementById('producto').value;
                    var productoError = document.getElementById('productoError');
                    if (producto === "") {
                        productoError.textContent = 'Por favor, selecciona un tipo de tinaco.';
                        productoError.style.display = 'block';
                        isValid = false;
                    } else {
                        productoError.textContent = '';
                        productoError.style.display = 'none';
                    }

                    var litros = document.getElementById('litros').value;
                    var litrosError = document.getElementById('litrosError');
                    var expresionlit = /^\d{1,3}\skg$/;

                    if (!expresionlit.test(litros)) {
                        litrosError.textContent = 'Por favor, ingresa una cantida en litros.';
                        litrosError.style.display = 'block';
                        isValid = false;
                    } else {
                        litrosError.textContent = '';
                        litrosError.style.display = 'none';
                    }


                    var color = document.getElementById('color').value;
                    var colorError = document.getElementById('colorError');
                    var expresioncol = /^\d{1,3}\skg$/;

                    if (!expresioncol.test(color)) {
                        colorError.textContent = 'Por favor, ingresa una nombre de color valido.';
                        colorError.style.display = 'block';
                        isValid = false;
                    } else {
                        colorError.textContent = '';
                        colorError.style.display = 'none';
                    }

                    var existencia = document.getElementById('existencia').value;
                    var existenciaError = document.getElementById('existenciaError');
                    var expresionexi = /^[0-9]{1,10}$/;

                    if (!expresionexi.test(existencia)) {
                        existenciaError.textContent = 'Por favor, ingresa un número. Sin espacios.';
                        existenciaError.style.display = 'block';
                        isValid = false;
                    } else {
                        existenciaError.textContent = '';
                        existenciaError.style.display = 'none';
                    }

                    

                    var precio = document.getElementById('precio').value;
                    var precioError = document.getElementById('precioError');
                    var expresionpre = /^\$[0-9]{1,10}$/;

                    if (!expresionpre.test(precio)) {
                        precioError.textContent = 'Por favor, ingresa un precio iniciando con el símbolo $. Sin espacios.';
                        precioError.style.display = 'block';
                        isValid = false;
                    } else {
                        precioError.textContent = '';
                        precioError.style.display = 'none';
                    }

                    var rotas = document.getElementById('rotas').value;
                    var rotasError = document.getElementById('rotasError');
                    var expresionerot = /^[0-9]{1,10}$/;
                        
                    if (!expresionerot.test(rotas)) {
                        rotasError.textContent = 'Por favor, ingresa un número. Sin espacios.';
                        rotasError.style.display = 'block';
                        isValid = false;
                    } else {
                        rotasError.textContent = '';
                        rotasError.style.display = 'none';
                    }

                    var ubicacion = document.getElementById('ubicacion').value;
                    var ubicacionError = document.getElementById('ubicacionError');
                    var expresionubi = /^[A-Z](?:[a-zA-Z0-9]+(?:\s[a-zA-Z0-9]+)*)?$/;

                    if (!expresionubi.test(ubicacion)) {
                        ubicacionError.textContent = 'Por favor, ingresa un número decimal seguido de "CJ". Sin espacios.';
                        ubicacionError.style.display = 'block';
                        isValid = false;
                    } else {
                        ubicacionError.textContent = '';
                        ubicacionError.style.display = 'none';
                    }



                    var proveedor = document.getElementById('proveedores').value;
                    var proveedorError = document.getElementById('proveedoresError');
                    if (proveedor === "") {
                        proveedorError.textContent = 'Por favor, selecciona un proveedor.';
                        proveedorError.style.display = 'block';
                        isValid = false;
                    } else {
                        proveedorError.textContent = '';
                        proveedorError.style.display = 'none';
                    }


                    var categorias = document.getElementById('categorias').value;
                    var categoriasError = document.getElementById('categoriasError');
                    if (categorias === "") {
                        categoriasError.textContent = 'Por favor, selecciona una categoría.';
                        categoriasError.style.display = 'block';
                        isValid = false;
                    } else {
                        categoriasError.textContent = '';
                        categoriasError.style.display = 'none';
                    }


                
                    return isValid;
                }
                


                // FUNCION PARA LA VALIDACION DEL FORMULARIO DE ACTUALIZAR 


                function validarFormularioproductoA() {
                    var isValid = true;
                
                    
                    var productoA = document.getElementById('productoeditar').value;
                    var productoErrorA = document.getElementById('productoErrorA');
                    if (productoA === "") {
                        productoErrorA.textContent = 'Por favor, selecciona un tipo de tinaco.';
                        productoErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        productoErrorA.textContent = '';
                        productoErrorA.style.display = 'none';
                    }

                    var litrosA = document.getElementById('litroseditar').value;
                    var litrosErrorA = document.getElementById('litrosErrorA');
                    var expresionlitA = /^\d{1,3}\skg$/;

                    if (!expresionlitA.test(litrosA)) {
                        litrosErrorA.textContent = 'Por favor, ingresa una cantida en litros.';
                        litrosErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        litrosErrorA.textContent = '';
                        litrosErrorA.style.display = 'none';
                    }


                    var colorA = document.getElementById('coloreditar').value;
                    var colorErrorA = document.getElementById('colorErrorA');
                    var expresioncolA = /^\d{1,3}\skg$/;

                    if (!expresioncolA.test(colorA)) {
                        colorErrorA.textContent = 'Por favor, ingresa una nombre de color valido.';
                        colorErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        colorErrorA.textContent = '';
                        colorErrorA.style.display = 'none';
                    }

                    var existenciaA = document.getElementById('existenciaeditar').value;
                    var existenciaErrorA = document.getElementById('existenciaErrorA');
                    var expresionexiA = /^[0-9]{1,10}$/;

                    if (!expresionexiA.test(existenciaA)) {
                        existenciaErrorA.textContent = 'Por favor, ingresa un número. Sin espacios.';
                        existenciaErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        existenciaErrorA.textContent = '';
                        existenciaErrorA.style.display = 'none';
                    }

                    var rotasA = document.getElementById('rotaseditar').value;
                    var rotasErrorA = document.getElementById('rotasErrorA');
                    var expresionerotA = /^[0-9]{1,10}$/;

                    if (!expresionerotA.test(rotasA)) {
                        rotasErrorA.textContent = 'Por favor, ingresa un número. Sin espacios.';
                        rotasErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        rotasErrorA.textContent = '';
                        rotasErrorA.style.display = 'none';
                    }


                    var precioA = document.getElementById('precioeditar').value;
                    var precioErrorA = document.getElementById('precioErrorA');
                    var expresionpreA = /^\$[0-9]{1,10}$/;

                    if (!expresionpreA.test(precioA)) {
                        precioErrorA.textContent = 'Por favor, ingresa un precio iniciando con el símbolo $. Sin espacios.';
                        precioErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        precioErrorA.textContent = '';
                        precioErrorA.style.display = 'none';
                    }

                    

                    var ubicacionA = document.getElementById('ubicacioneditar').value;
                    var ubicacionErrorA = document.getElementById('ubicacionErrorA');
                    var expresionubiA = /^[A-Z](?:[a-zA-Z0-9]+(?:\s[a-zA-Z0-9]+)*)?$/;

                    if (!expresionubiA.test(ubicacionA)) {
                        ubicacionErrorA.textContent = 'Por favor, ingresa un número decimal seguido de "CJ". Sin espacios.';
                        ubicacionErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        ubicacionErrorA.textContent = '';
                        ubicacionErrorA.style.display = 'none';
                    }



                    var proveedorA = document.getElementById('proveedoreseditar').value;
                    var proveedorErrorA = document.getElementById('proveedoresErrorA');
                    if (proveedorA === "") {
                        proveedorErrorA.textContent = 'Por favor, selecciona un proveedor.';
                        proveedorErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        proveedorErrorA.textContent = '';
                        proveedorErrorA.style.display = 'none';
                    }


                    var categoriasA = document.getElementById('categoriaseditar').value;
                    var categoriasErrorA = document.getElementById('categoriasErrorA');
                    if (categoriasA === "") {
                        categoriasErrorA.textContent = 'Por favor, selecciona una categoría.';
                        categoriasErrorA.style.display = 'block';
                        isValid = false;
                    } else {
                        categoriasErrorA.textContent = '';
                        categoriasErrorA.style.display = 'none';
                    }


                
                    return isValid;
                }


                