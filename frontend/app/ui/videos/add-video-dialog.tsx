import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogClose,
  } from "@/components/ui/dialog";
  import { Button } from "@/components/ui/button";
  import { Input } from "@/components/ui/input";
  import { Label } from "@/components/ui/label";
  import { addVideo } from "@/app/lib/actions";
  
  export default function AddVideoDialog() {
    return (
      <Dialog>
        <DialogTrigger asChild>
          <Button>Add Video</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Add Video</DialogTitle>
            <DialogDescription>
              Add a link to the video that you want to add
            </DialogDescription>
          </DialogHeader>
          <form className="grid gap-4" action={addVideo}>
            <div className="grid gap-2">
              <Label htmlFor="videoUrl">URL</Label>
              <Input id="videoUrl" name="videoUrl" className="col-span-3" />
            </div>
            <DialogFooter>
              <DialogClose asChild>
                <Button type="submit">Save Video</Button>
              </DialogClose>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    );
  }
  