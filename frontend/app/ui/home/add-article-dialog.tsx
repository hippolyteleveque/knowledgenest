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
import { addArticle } from "@/app/lib/actions";

export default function AddArticleDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Add Article</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Article</DialogTitle>
          <DialogDescription>
            Add a link to the article that you want to add
          </DialogDescription>
        </DialogHeader>
        <form className="grid gap-4" action={addArticle}>
          <div className="grid gap-2">
            <Label htmlFor="articleUrl">URL</Label>
            <Input id="articleUrl" name="articleUrl" className="col-span-3" />
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button type="submit">Save Article</Button>
            </DialogClose>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
