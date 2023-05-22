using Microsoft.AspNetCore.Mvc;
using Microsoft.Win32;
using System.Diagnostics;
using TravIS.Models;

namespace TravIS.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        private string run_cmd(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = @"C:\Users\Dominik\AppData\Local\Microsoft\WindowsApps\python3.10.exe";
            start.Arguments = string.Format("{0} {1}", cmd, args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;

            using (Process process = Process.Start(start))
            using (StreamReader reader = process.StandardOutput)
                return reader.ReadToEnd().ReplaceLineEndings("");

        }


        [HttpPost]
        public IActionResult Result(IFormCollection collection)
        {
            string keywords = collection["keywords"];
            if (string.IsNullOrEmpty(keywords))
                return RedirectToAction("Index");

            string result = run_cmd(@"C:\Users\Dominik\source\repos\piccolino1\TravIS\Python\Finder\Finder.py", '"' + keywords.Replace('"', ' ') + '"');

            return View(
                new ResultViewModel() { 
                    Country = result 
                });
        }

        public IActionResult Pricing()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}