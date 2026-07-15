using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using tp04.Models;

namespace tp04.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    private bd BD = new bd();

    public IActionResult Index()
    {
        ViewBag.Figuritas = BD.ObtenerFiguritas();
        return View();
    }
[HttpGet]
public IActionResult AbrirPaquete()
{
    return View();
}

[HttpPost]
public IActionResult GenerarSobre()
{
    ViewBag.SobreFigus = BD.ObtenerSobre();
    
    return View("AbrirPaquete");
}
 [HttpPost]
public IActionResult pegarFigurita(List<int> ids)
{
    List<Figurita> figuritas = BD.ObtenerFiguritas(ids);

    BD.PegarFigu(figuritas);

    return View("AbrirPaquete");
}

    

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}
